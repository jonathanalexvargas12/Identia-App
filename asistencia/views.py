import json
import logging
from datetime import datetime, date, time, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from config.decorators import role_required

logger = logging.getLogger(__name__)

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def obtener_horario_usuario(usuario_id, fecha):
    """
    Retorna el horario aplicable para un usuario en una fecha específica.
    Busca primero por tipo_fk y fecha exacta, luego por tipo_fk y fecha NULL.
    Devuelve un dict con hora_entrada, tolerancia_entrada, hora_salida, tolerancia_salida,
    o None si no hay horario.
    """
    with connection.cursor() as cursor:
        # Obtener tipo_fk del usuario
        cursor.execute("SELECT tipo_fk FROM usuarios WHERE id_pk = %s", [usuario_id])
        row = cursor.fetchone()
        if not row:
            logger.warning(f"Usuario {usuario_id} no encontrado")
            return None
        tipo_fk = row[0]

        # Buscar horario con fecha exacta
        cursor.execute("""
            SELECT hora_entrada, tolerancia_entrada, hora_salida, tolerancia_salida
            FROM horarios_jornada
            WHERE tipo_fk = %s AND fecha = %s
        """, [tipo_fk, fecha])
        row = cursor.fetchone()
        if row:
            return {
                'hora_entrada': row[0],
                'tolerancia_entrada': int(row[1]) if row[1] is not None else 0,
                'hora_salida': row[2],
                'tolerancia_salida': int(row[3]) if row[3] is not None else 0,
            }

        # Buscar horario genérico (fecha NULL)
        cursor.execute("""
            SELECT hora_entrada, tolerancia_entrada, hora_salida, tolerancia_salida
            FROM horarios_jornada
            WHERE tipo_fk = %s AND fecha IS NULL
        """, [tipo_fk])
        row = cursor.fetchone()
        if row:
            return {
                'hora_entrada': row[0],
                'tolerancia_entrada': int(row[1]) if row[1] is not None else 0,
                'hora_salida': row[2],
                'tolerancia_salida': int(row[3]) if row[3] is not None else 0,
            }

    logger.info(f"No hay horario definido para tipo '{tipo_fk}' en fecha {fecha}")
    return None


def calcular_estado_entrada(hora_acceso, fecha, horario):
    """
    Compara la hora de acceso con la hora de entrada + tolerancia en la fecha dada.
    Retorna 'Presente' si está dentro de la tolerancia, 'Tardanza' si es después.
    Si no hay horario, retorna 'Presente' por defecto.
    """
    if not horario or not horario.get('hora_entrada'):
        return 'Presente'

    entrada_teorica = datetime.combine(fecha, horario['hora_entrada'])
    acceso_dt = datetime.combine(fecha, hora_acceso)
    tolerancia = horario.get('tolerancia_entrada', 0)

    limite = entrada_teorica + timedelta(minutes=tolerancia)

    if acceso_dt <= limite:
        return 'Presente'
    else:
        return 'Tardanza'


def cerrar_jornadas_incompletas(usuario_id, fecha_actual):
    """
    Busca registros de días anteriores (fecha < fecha_actual) con hora_salida NULL
    y los cierra marcándolos como 'Jornada incompleta'.
    Asigna como hora_salida la hora de salida teórica del horario del usuario para esa fecha,
    o 23:59:59 si no hay horario.
    """
    with connection.cursor() as cursor:
        # Obtener todos los registros abiertos de días anteriores
        cursor.execute("""
            SELECT id_pk, fecha FROM bitacora_asistencia
            WHERE id_usuario_fk = %s AND fecha < %s AND hora_salida IS NULL
        """, [usuario_id, fecha_actual])
        registros_abiertos = cursor.fetchall()

        for reg_id, fecha_reg in registros_abiertos:
            # Obtener horario para esa fecha
            horario = obtener_horario_usuario(usuario_id, fecha_reg)
            if horario and horario.get('hora_salida'):
                hora_fin = horario['hora_salida']
            else:
                # Si no hay horario, usar 23:59:59
                hora_fin = time(23, 59, 59)

            cursor.execute("""
                UPDATE bitacora_asistencia
                SET salida = 'Salida', hora_salida = %s, estado_jornada = 'Jornada incompleta'
                WHERE id_pk = %s
            """, [hora_fin, reg_id])
            logger.info(f"Jornada incompleta cerrada para registro ID {reg_id} (fecha {fecha_reg})")


def registrar_acceso(usuario_id, fecha, hora, tipo_acceso, horario=None):
    """
    Función principal para registrar una entrada o salida en la bitácora.
    tipo_acceso: 'entrada' o 'salida'
    Retorna el ID del registro creado/actualizado o None si error.
    Maneja múltiples pares por día y etiqueta salidas parciales/fuera de jornada.
    """
    try:
        with connection.cursor() as cursor:
            if tipo_acceso == 'entrada':
                # Antes de insertar una nueva entrada, cerrar jornadas incompletas de días anteriores
                cerrar_jornadas_incompletas(usuario_id, fecha)

                # Buscar el último registro del día
                cursor.execute("""
                    SELECT id_pk, hora_salida, salida FROM bitacora_asistencia
                    WHERE id_usuario_fk = %s AND fecha = %s
                    ORDER BY hora_acceso DESC LIMIT 1
                """, [usuario_id, fecha])
                ultimo = cursor.fetchone()

                # Si hay un último registro con hora_salida no nula, o no hay registro, creamos nueva entrada
                if not ultimo or ultimo[1] is not None:
                    # Determinar el estado de la nueva entrada
                    if ultimo is None:
                        # Primera entrada del día: calcular según horario
                        if horario is None:
                            horario = obtener_horario_usuario(usuario_id, fecha)
                        estado = calcular_estado_entrada(hora, fecha, horario)
                    else:
                        # Ya hay registros hoy y el último tiene salida: es un regreso
                        estado = 'Regreso'

                    cursor.execute("""
                        INSERT INTO bitacora_asistencia
                        (id_usuario_fk, acceso, hora_acceso, fecha, estado_jornada)
                        VALUES (%s, 'Entrada', %s, %s, %s)
                    """, [usuario_id, hora, fecha, estado])
                    nuevo_id = cursor.lastrowid
                    logger.info(f"Entrada registrada ID {nuevo_id} para usuario {usuario_id} con estado {estado}")

                    # Si había un último registro con salida, y esa salida era normal (no fuera jornada), la convertimos en parcial
                    if ultimo and ultimo[1] is not None:
                        if ultimo[2] == 'Salida' or ultimo[2] is None:
                            cursor.execute("""
                                UPDATE bitacora_asistencia
                                SET salida = 'Salida parcial'
                                WHERE id_pk = %s
                            """, [ultimo[0]])
                            logger.info(f"Salida anterior ID {ultimo[0]} marcada como parcial")
                    connection.commit()
                    return nuevo_id
                else:
                    # Hay una entrada sin salida, no se puede registrar otra entrada
                    logger.warning(f"Intento de entrada duplicada para usuario {usuario_id} el {fecha}")
                    return None

            elif tipo_acceso == 'salida':
                # Buscar el último registro con hora_salida nula
                cursor.execute("""
                    SELECT id_pk FROM bitacora_asistencia
                    WHERE id_usuario_fk = %s AND fecha = %s AND hora_salida IS NULL
                    ORDER BY hora_acceso DESC LIMIT 1
                """, [usuario_id, fecha])
                registro = cursor.fetchone()
                if not registro:
                    logger.warning(f"Intento de salida sin entrada previa para usuario {usuario_id} el {fecha}")
                    return None

                # Determinar tipo de salida según horario
                if horario is None:
                    horario = obtener_horario_usuario(usuario_id, fecha)
                tipo_salida = 'Salida'  # por defecto
                if horario and horario.get('hora_salida'):
                    # Calcular si está fuera de jornada
                    salida_teorica = datetime.combine(fecha, horario['hora_salida'])
                    salida_dt = datetime.combine(fecha, hora)
                    tolerancia_salida = horario.get('tolerancia_salida', 0)
                    limite_salida = salida_teorica + timedelta(minutes=tolerancia_salida)
                    if salida_dt > limite_salida:
                        tipo_salida = 'Salida fuera jornada'

                cursor.execute("""
                    UPDATE bitacora_asistencia
                    SET salida = %s, hora_salida = %s
                    WHERE id_pk = %s
                """, [tipo_salida, hora, registro[0]])
                connection.commit()
                logger.info(f"Salida registrada para registro ID {registro[0]} tipo {tipo_salida}")
                return registro[0]
    except Exception as e:
        logger.error(f"Error en registrar_acceso: {str(e)}")
        return None


# ============================================================================
# VISTAS CRUD
# ============================================================================

@login_required
@role_required('Administrador', 'Seguridad')
def lista_asistencia_view(request):
    """
    Lista los registros de asistencia con filtros por fecha y usuario.
    """
    fecha_desde = request.GET.get('desde', '')
    fecha_hasta = request.GET.get('hasta', '')
    usuario_id = request.GET.get('usuario', '')

    query = """
        SELECT ba.id_pk, ba.fecha, ba.hora_acceso, ba.hora_salida,
               ba.estado_jornada, u.cedula, u.nombres, u.apellidos, u.tipo_fk
        FROM bitacora_asistencia ba
        JOIN usuarios u ON ba.id_usuario_fk = u.id_pk
        WHERE 1=1
    """
    params = []

    if fecha_desde:
        query += " AND ba.fecha >= %s"
        params.append(fecha_desde)
    if fecha_hasta:
        query += " AND ba.fecha <= %s"
        params.append(fecha_hasta)
    if usuario_id:
        query += " AND u.id_pk = %s"
        params.append(usuario_id)

    query += " ORDER BY ba.fecha DESC, ba.hora_acceso DESC"

    registros = []
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        for row in cursor.fetchall():
            registros.append(dict(zip(columns, row)))

    # Obtener lista de usuarios para el filtro
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_pk, cedula, nombres, apellidos FROM usuarios ORDER BY apellidos, nombres")
        usuarios = [{'id': r[0], 'cedula': r[1], 'nombre': f"{r[2]} {r[3]}"} for r in cursor.fetchall()]

    # ==============================================
    # PAGINACIÓN: 10 REGISTROS POR PÁGINA
    # ==============================================
    registros_por_pagina = 10
    paginator = Paginator(registros, registros_por_pagina)
    page = request.GET.get('page', 1)

    try:
        registros_paginados = paginator.page(page)
    except PageNotAnInteger:
        registros_paginados = paginator.page(1)
    except EmptyPage:
        registros_paginados = paginator.page(paginator.num_pages)

    # Calcular información de paginación
    if registros_paginados:
        inicio = (registros_paginados.number - 1) * registros_por_pagina + 1
        fin = inicio + len(registros_paginados.object_list) - 1
        rango_mostrado = f"{inicio}-{fin}"
    else:
        rango_mostrado = "0-0"

    total_registros = len(registros)
    total_paginas = paginator.num_pages

    context = {
        'page_title': 'Bitácora de Asistencia',
        'menu_activo': 'asistencia',
        'registros': registros_paginados,
        'usuarios': usuarios,
        'filtro_desde': fecha_desde,
        'filtro_hasta': fecha_hasta,
        'filtro_usuario': usuario_id,
        'hoy': date.today(),
        'total_registros': total_registros,
        'total_paginas': total_paginas,
        'pagina_actual': registros_paginados.number,
        'rango_mostrado': rango_mostrado,
        'registros_por_pagina': registros_por_pagina,
    }
    return render(request, 'asistencia/bitacora_asistencia.html', context)


@login_required
@role_required('Administrador', 'Seguridad')
def detalle_asistencia_view(request, registro_id):
    """
    Muestra el detalle de un registro de asistencia.
    Si es AJAX, devuelve solo el contenido de la tarjeta (sin layout base).
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ba.id_pk, ba.fecha, ba.hora_acceso, ba.hora_salida,
                   ba.estado_jornada, ba.acceso, ba.salida,
                   u.id_pk, u.cedula, u.nombres, u.apellidos, u.tipo_fk
            FROM bitacora_asistencia ba
            JOIN usuarios u ON ba.id_usuario_fk = u.id_pk
            WHERE ba.id_pk = %s
        """, [registro_id])
        row = cursor.fetchone()
        if not row:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Registro no encontrado'}, status=404)
            messages.error(request, "Registro no encontrado")
            return redirect('asistencia:lista')

    registro = {
        'id': row[0],
        'fecha': row[1],
        'hora_acceso': row[2],
        'hora_salida': row[3],
        'estado': row[4],
        'acceso': row[5],
        'salida': row[6],
        'usuario_id': row[7],
        'cedula': row[8],
        'nombres': row[9],
        'apellidos': row[10],
        'tipo': row[11],
    }

    context = {
        'page_title': f"Detalle de asistencia - {registro['cedula']}",
        'menu_activo': 'asistencia',
        'registro': registro,
    }

    # Si es una petición AJAX, renderizar solo el contenido del modal
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'asistencia/detalle_asistencia.html', context)
    
    # Si no, renderizar la página completa
    return render(request, 'asistencia/detalle_asistencia.html', context)