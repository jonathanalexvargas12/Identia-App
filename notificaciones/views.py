"""
Vistas para el módulo de Notificaciones/Bitácora.
Muestra el registro de todos los incidentes del sistema.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from datetime import datetime, timedelta
import logging
import json
from config.decorators import role_required
from reportes.views import crear_pdf, get_datos_incidentes

# ==============================================
# IMPORTAR FUNCIONES DE UTILS
# ==============================================
try:
    from .utils import get_client_ip
    UTILS_DISPONIBLE = True
except ImportError:
    # Fallback si no existe utils.py
    UTILS_DISPONIBLE = False
    def get_client_ip(request): 
        """Fallback: obtener IP de REMOTE_ADDR"""
        return request.META.get('REMOTE_ADDR', '0.0.0.0')
    print("ADVERTENCIA: Función get_client_ip no disponible en notificaciones/views.py - usando fallback")

logger = logging.getLogger(__name__)

# ==============================================
# CONSTANTES PARA NOTIFICACIONES
# ==============================================
TIPOS_NOTIFICACION = ['login', 'logout', 'agregar', 'editar', 'eliminar', 'activar', 'desactivar']

ICONOS_POR_TIPO = {
    'login': '🔓',
    'logout': '🔒',
    'agregar': '➕',
    'editar': '✏️',
    'eliminar': '🗑️',
    'activar': '✅',
    'desactivar': '⚠️',
    'otro': '📌'
}

COLORES_POR_TIPO = {
    'login': '#27ae60',
    'logout': '#e67e22',
    'agregar': '#2ecc71',
    'editar': '#3498db',
    'eliminar': '#e74c3c',
    'activar': '#27ae60',
    'desactivar': '#f39c12',
    'otro': '#95a5a6'
}


def determinar_tipo_evento(novedad):
    """Determina el tipo de evento basado en la novedad"""
    if not novedad:
        return 'otro'
    
    n = novedad.upper()
    
    if 'INICIO' in n and ('SESION' in n or 'SESIÓN' in n):
        return 'login'
    elif 'CIERRE' in n and ('SESION' in n or 'SESIÓN' in n):
        return 'logout'
    elif 'AGREGÓ' in n or 'AGREGO' in n:
        return 'agregar'
    elif 'EDITÓ' in n or 'EDITO' in n or 'ACTUALIZÓ' in n or 'ACTUALIZO' in n:
        return 'editar'
    elif 'ELIMINÓ' in n or 'ELIMINO' in n:
        return 'eliminar'
    elif 'ACTIVÓ' in n or 'ACTIVO' in n:
        return 'activar'
    elif 'DESACTIVÓ' in n or 'DESACTIVO' in n:
        return 'desactivar'
    elif 'DETECTAR' in n and 'DUPLICADOS' in n:
        return 'duplicado'
    elif 'AJUSTAR' in n and 'UMBRAL' in n:
        return 'configuracion'
    else:
        return 'otro'
    
    n = novedad.upper()
    
    if 'INICIO' in n and ('SESION' in n or 'SESIÓN' in n):
        return 'login'
    elif 'CIERRE' in n and ('SESION' in n or 'SESIÓN' in n):
        return 'logout'
    elif 'AGREGO' in n:
        return 'agregar'
    elif 'EDITO' in n or 'ACTUALIZO' in n:
        return 'editar'
    elif 'ELIMINO' in n:
        return 'eliminar'
    elif 'ACTIVO' in n:
        return 'activar'
    elif 'DESACTIVO' in n:
        return 'desactivar'
    elif 'DETECTAR' in n and 'DUPLICADOS' in n:
        return 'duplicado'
    elif 'AJUSTAR' in n and 'UMBRAL' in n:
        return 'configuracion'
    else:
        return 'otro'
    
    novedad_upper = novedad.upper()
    
    if 'INICIO' in novedad_upper and 'SESIÓN' in novedad_upper:
        return 'login'
    elif 'CIERRE' in novedad_upper and 'SESIÓN' in novedad_upper:
        return 'logout'
    elif 'AGREGÓ' in novedad_upper:
        return 'agregar'
    elif 'EDITÓ' in novedad_upper or 'ACTUALIZÓ' in novedad_upper:
        return 'editar'
    elif 'ELIMINÓ' in novedad_upper:
        return 'eliminar'
    elif 'ACTIVÓ' in novedad_upper:
        return 'activar'
    elif 'DESACTIVÓ' in novedad_upper:
        return 'desactivar'
    elif 'CAMBIÓ' in novedad_upper:
        return 'cambiar'
    elif 'DETECTAR' in novedad_upper and 'DUPLICADOS' in novedad_upper:
        return 'duplicado'
    elif 'AJUSTAR' in novedad_upper and 'UMBRAL' in novedad_upper:
        return 'configuracion'
    else:
        return 'otro'


def generar_url_notificacion(tipo, incidente_id, detalles):
    """
    Genera la URL de redirección según el tipo de notificación.
    """
    try:
        if tipo == 'login' or tipo == 'logout':
            return '/usuarios/dashboard/'
        
        # Buscar ID de usuario/trabajador en los detalles
        import re
        match_id = re.search(r'ID: (\d+)', detalles)
        
        if tipo in ['agregar', 'editar', 'eliminar', 'activar', 'desactivar']:
            if 'TRABAJADORES' in detalles or 'trabajador' in detalles.lower():
                if match_id:
                    return f'/reconocimiento/gestion-trabajadores/?id={match_id.group(1)}'
                return '/reconocimiento/gestion-trabajadores/'
            
            elif 'TIPOS_PERSONAL' in detalles or 'Tipo' in detalles:
                if 'actualizado de' in detalles.lower():
                    # Extraer nombre del tipo
                    match_tipo = re.search(r"de '([^']+)' a '([^']+)'", detalles)
                    if match_tipo:
                        return f'/usuarios/gestion-tipos-personal/?accion=editar&id={match_tipo.group(2)}'
                return '/usuarios/gestion-tipos-personal/'
            
            elif 'HORARIOS' in detalles or 'Horario' in detalles:
                if match_id:
                    return f'/usuarios/gestion-horarios/?id={match_id.group(1)}'
                return '/usuarios/gestion-horarios/'
            
            elif 'PERFIL' in detalles:
                return '/usuarios/perfil/'
            
            elif 'ROSTROS' in detalles or 'rostro' in detalles.lower():
                if match_id:
                    return f'/reconocimiento/gestion-trabajadores/?id={match_id.group(1)}'
                return '/reconocimiento/gestion-trabajadores/'
            
            elif 'CONFIGURACIÓN' in detalles or 'Umbral' in detalles:
                return '/reconocimiento/control_acceso/'
            
            elif 'DUPLICADOS' in detalles:
                return '/reconocimiento/gestion-trabajadores/'
        
        return '#'
    except:
        return '#'


def resumir_detalles(detalles, max_length=60):
    """Resume los detalles para mostrar en notificaciones"""
    if not detalles:
        return ''
    if len(detalles) <= max_length:
        return detalles
    return detalles[:max_length] + '...'


# ==============================================
# FUNCIONES DE ACCESO A BASE DE DATOS
# ==============================================

def obtener_id_usuario_real(request):
    """
    Obtiene el ID real del usuario desde la tabla 'usuarios' usando la sesión.
    """
    # Intentar obtener de la sesión (donde se guarda en login)
    empleado_id = request.session.get('empleado_id')
    if empleado_id:
        return empleado_id
    
    # Fallback: buscar por username (que es la cédula)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_pk FROM usuarios WHERE cedula = %s
            """, [request.user.username])
            result = cursor.fetchone()
            if result:
                return result[0]
    except Exception as e:
        logger.error(f"Error obteniendo ID real de usuario: {str(e)}")
    
    return None


def obtener_notificaciones_leidas(usuario_id):
    """
    Obtiene los IDs de incidentes leídos por un usuario desde la BD.
    """
    if not usuario_id:
        return []
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_incidente_fk 
                FROM notificaciones_leidas 
                WHERE id_usuario_fk = %s
            """, [usuario_id])
            return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Error obteniendo notificaciones leídas: {str(e)}")
        return []


def marcar_notificacion_como_leida(usuario_id, incidente_id):
    """
    Marca una notificación como leída en la BD.
    """
    if not usuario_id:
        logger.error("No se pudo marcar como leída: usuario_id es None")
        return False
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT IGNORE INTO notificaciones_leidas 
                (id_usuario_fk, id_incidente_fk, fecha_lectura) 
                VALUES (%s, %s, NOW())
            """, [usuario_id, incidente_id])
            connection.commit()
            logger.info(f"Notificación {incidente_id} marcada como leída para usuario {usuario_id}")
        return True
    except Exception as e:
        logger.error(f"Error marcando notificación como leída: {str(e)}")
        return False


def contar_notificaciones_no_leidas(usuario_id):
    """
    Cuenta las notificaciones no leídas de un usuario.
    """
    if not usuario_id:
        return 0
    
    try:
        # Obtener IDs de notificaciones leídas
        leidas = obtener_notificaciones_leidas(usuario_id)
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_pk, novedad
                FROM bitacora_incidentes
                ORDER BY fecha DESC, hora DESC
                LIMIT 100
            """)
            
            no_leidas = 0
            for row in cursor.fetchall():
                tipo = determinar_tipo_evento(row[1] or '')
                if tipo in TIPOS_NOTIFICACION:
                    if leidas and row[0] in leidas:
                        continue
                    no_leidas += 1
            
            return no_leidas
    except Exception as e:
        logger.error(f"Error contando notificaciones no leídas: {str(e)}")
        return 0


@login_required
@role_required('Administrador', 'Seguridad')
def bitacora_incidentes_view(request):
    """
    Vista principal de la bitácora de incidentes.
    Muestra todos los registros de la tabla bitacora_incidentes con filtros.
    PAGINACIÓN: EXACTAMENTE 10 REGISTROS POR PÁGINA.
    """
    # Obtener ID real del usuario
    usuario_id = obtener_id_usuario_real(request)
    
    # Obtener parámetros de filtro
    fecha_desde = request.GET.get('fecha_desde', '').strip()
    fecha_hasta = request.GET.get('fecha_hasta', '').strip()
    search_query = request.GET.get('search', '').strip()
    solo_no_leidas = request.GET.get('no_leidas', '') == '1'
    
    # La bitácora de incidentes SIEMPRE muestra todos los registros (no filtra por leídas)
    # El parámetro no_leidas se ignora para mantener auditoría completa
    # solo_no_leidas = False
    
    # Construir consulta base - SIN formatear en SQL
    query = """
        SELECT 
            id_pk,
            novedad,
            detalles,
            hora,
            fecha,
            ip
        FROM bitacora_incidentes
        WHERE 1=1
    """
    params = []
    
    # Aplicar filtros
    if fecha_desde:
        query += " AND fecha >= %s"
        params.append(fecha_desde)
    
    if fecha_hasta:
        query += " AND fecha <= %s"
        params.append(fecha_hasta)
    
    if search_query:
        query += """ AND (
            novedad LIKE %s OR 
            detalles LIKE %s OR 
            ip LIKE %s
        )"""
        search_param = f"%{search_query}%"
        params.extend([search_param, search_param, search_param])
    
    # Ordenar por fecha y hora descendente (más reciente primero)
    query += " ORDER BY fecha DESC, hora DESC"
    
    # Ejecutar consulta
    incidentes = []
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Obtener notificaciones leídas desde BD
            notificaciones_leidas = obtener_notificaciones_leidas(usuario_id) if usuario_id else []
            
            for row in rows:
                id_pk, novedad, detalles, hora, fecha, ip = row
                
                tipo = determinar_tipo_evento(novedad or '')
                
                # Formatear fecha y hora en Python
                fecha_formateada = fecha.strftime('%d/%m/%Y') if fecha else ''
                hora_formateada = hora.strftime('%H:%M:%S') if hora else ''
                
                # Extraer posible ID de usuario de los detalles (opcional)
                usuario_info = "Sistema"
                if detalles and ("Usuario ID:" in detalles or "C.I:" in detalles):
                    if "Usuario" in detalles:
                        partes = detalles.split("Usuario")
                        if len(partes) > 1:
                            usuario_info = "Usuario" + partes[1].split(" en ")[0]
                
                incidentes.append({
                    'id': id_pk,
                    'novedad': novedad or '',
                    'detalles': detalles or '',
                    'detalles_resumido': resumir_detalles(detalles or ''),
                    'hora': hora_formateada,
                    'fecha': fecha_formateada,
                    'fecha_raw': fecha,
                    'hora_raw': hora,
                    'ip': ip or 'No registrada',
                    'usuario_info': usuario_info,
                    'tipo': tipo,
                    'leida': id_pk in notificaciones_leidas if notificaciones_leidas else False,
                    'icono': ICONOS_POR_TIPO.get(tipo, '📌'),
                    'color': COLORES_POR_TIPO.get(tipo, '#95a5a6'),
                    'url': generar_url_notificacion(tipo, id_pk, detalles or '')
                })
    except Exception as e:
        logger.error(f"Error obteniendo bitácora: {str(e)}")
        incidentes = []
    
    # La bitácora de incidentes SIEMPRE muestra todos los registros
    # (no se filtra por leídas para mantener auditoría completa)
    # if solo_no_leidas:
    #     incidentes = [inc for inc in incidentes if not inc['leida'] and inc['tipo'] in TIPOS_NOTIFICACION]
    
    # ==============================================
    # PAGINACIÓN: EXACTAMENTE 10 REGISTROS POR PÁGINA
    # ==============================================
    registros_por_pagina = 10
    paginator = Paginator(incidentes, registros_por_pagina)
    page = request.GET.get('page', 1)
    
    try:
        incidentes_paginados = paginator.page(page)
    except PageNotAnInteger:
        incidentes_paginados = paginator.page(1)
    except EmptyPage:
        incidentes_paginados = paginator.page(paginator.num_pages)
    
    # Calcular rango de registros mostrados
    if incidentes_paginados:
        inicio = (incidentes_paginados.number - 1) * registros_por_pagina + 1
        fin = inicio + len(incidentes_paginados.object_list) - 1
        rango_mostrado = f"{inicio}-{fin}"
    else:
        rango_mostrado = "0-0"
    
    # Estadísticas rápidas
    total_registros = len(incidentes)
    total_paginas = paginator.num_pages
    
    # Contar por tipo de evento
    tipos_conteo = {}
    for inc in incidentes:
        tipo = inc['tipo']
        tipos_conteo[tipo] = tipos_conteo.get(tipo, 0) + 1
    
    # Contar no leídas (usando la función de BD)
    no_leidas = contar_notificaciones_no_leidas(usuario_id) if usuario_id else 0
    
    # Obtener IP del request actual
    ip_actual = get_client_ip(request)
    
    context = {
        'page_title': 'Bitácora de Incidentes - Sistema de Auditoría',
        'menu_activo': 'notificaciones',
        'incidentes': incidentes_paginados,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'search_query': search_query,
        'total_registros': total_registros,
        'total_paginas': total_paginas,
        'pagina_actual': incidentes_paginados.number,
        'rango_mostrado': rango_mostrado,
        'registros_por_pagina': registros_por_pagina,
        'tipos_conteo': tipos_conteo,
        'hoy': datetime.now().date(),
        'semana_pasada': (datetime.now() - timedelta(days=7)).date(),
        'ip_actual': ip_actual,
        'no_leidas': no_leidas,
        'solo_no_leidas': solo_no_leidas,
    }
    
    return render(request, 'notificaciones/bitacora_incidentes.html', context)


# ==============================================
# PDF DE BITÁCORA
# ==============================================

@login_required
@role_required('Administrador', 'Seguridad')
def bitacora_pdf(request):
    """Genera PDF completo de la bitácora de incidentes"""
    titulo = 'Bitácora de Incidentes'
    columnas, datos = get_datos_incidentes(None, '', '')
    return crear_pdf(titulo, columnas, datos, 'Completo')


# ==============================================
# API PARA NOTIFICACIONES
# ==============================================

@login_required
@role_required('Administrador', 'Seguridad')
def api_notificaciones(request):
    """
    API para obtener las últimas 5 notificaciones.
    """
    try:
        # Obtener ID real del usuario
        usuario_id = obtener_id_usuario_real(request)
        
        # Siempre traer las últimas 5
        limite = 5
        
        # Consultar últimos incidentes
        query = """
            SELECT 
                id_pk,
                novedad,
                detalles,
                hora,
                fecha
            FROM bitacora_incidentes
            ORDER BY fecha DESC, hora DESC
            LIMIT %s
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query, [limite * 2])  # Traer 10 para filtrar después
            rows = cursor.fetchall()
            
            # Obtener notificaciones leídas desde BD
            notificaciones_leidas = obtener_notificaciones_leidas(usuario_id) if usuario_id else []
            
            notificaciones = []
            for row in rows:
                id_pk, novedad, detalles, hora, fecha = row
                
                tipo = determinar_tipo_evento(novedad or '')
                
                # Solo incluir tipos relevantes
                if tipo not in TIPOS_NOTIFICACION:
                    continue
                
                # Formatear fecha y hora en Python
                fecha_formateada = fecha.strftime('%d/%m/%Y') if fecha else ''
                hora_formateada = hora.strftime('%H:%M') if hora else ''
                
                notificaciones.append({
                    'id': id_pk,
                    'novedad': novedad or '',
                    'detalles': detalles or '',
                    'detalles_resumido': resumir_detalles(detalles or ''),
                    'hora': hora_formateada,
                    'fecha_formateada': fecha_formateada,
                    'fecha': str(fecha) if fecha else '',
                    'hora_raw': str(hora) if hora else '',
                    'tipo': tipo,
                    'leida': id_pk in notificaciones_leidas if notificaciones_leidas else False,
                    'icono': ICONOS_POR_TIPO.get(tipo, '📌'),
                    'color': COLORES_POR_TIPO.get(tipo, '#95a5a6'),
                    'url': generar_url_notificacion(tipo, id_pk, detalles or '')
                })
                
                # Limitar a 5
                if len(notificaciones) >= limite:
                    break
            
            # Contar no leídas
            no_leidas = contar_notificaciones_no_leidas(usuario_id) if usuario_id else 0
            
            return JsonResponse({
                'success': True,
                'notificaciones': notificaciones,
                'no_leidas': no_leidas,
                'total': len(notificaciones)
            })
            
    except Exception as e:
        logger.error(f"Error en api_notificaciones: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@role_required('Administrador', 'Seguridad')
def api_contador_no_leidas(request):
    """
    API para obtener solo el contador de notificaciones no leídas.
    """
    try:
        usuario_id = obtener_id_usuario_real(request)
        no_leidas = contar_notificaciones_no_leidas(usuario_id) if usuario_id else 0
        return JsonResponse({'success': True, 'no_leidas': no_leidas})
            
    except Exception as e:
        logger.error(f"Error en api_contador_no_leidas: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@role_required('Administrador', 'Seguridad')
def api_marcar_leida(request):
    """
    API para marcar una notificación como leída (GUARDADO EN BD).
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        notificacion_id = data.get('id')
        
        if not notificacion_id:
            return JsonResponse({'success': False, 'error': 'ID requerido'}, status=400)
        
        # Obtener ID real del usuario
        usuario_id = obtener_id_usuario_real(request)
        
        if not usuario_id:
            return JsonResponse({
                'success': False, 
                'error': 'No se pudo identificar al usuario en la tabla usuarios'
            }, status=400)
        
        # Guardar en base de datos
        marcar_notificacion_como_leida(usuario_id, notificacion_id)
        
        # Recalcular contador
        no_leidas = contar_notificaciones_no_leidas(usuario_id)
        
        return JsonResponse({'success': True, 'no_leidas': no_leidas})
        
    except Exception as e:
        logger.error(f"Error en api_marcar_leida: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@role_required('Administrador', 'Seguridad')
def api_marcar_todas_leidas(request):
    """
    API para marcar todas las notificaciones como leídas.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)
    
    try:
        # Obtener ID real del usuario
        usuario_id = obtener_id_usuario_real(request)
        
        if not usuario_id:
            return JsonResponse({
                'success': False, 
                'error': 'No se pudo identificar al usuario en la tabla usuarios'
            }, status=400)
        
        with connection.cursor() as cursor:
            # Obtener todas las notificaciones no leídas (solo las que faltan)
            cursor.execute("""
                SELECT id_pk, novedad
                FROM bitacora_incidentes bi
                WHERE NOT EXISTS (
                    SELECT 1 
                    FROM notificaciones_leidas nl 
                    WHERE nl.id_incidente_fk = bi.id_pk 
                    AND nl.id_usuario_fk = %s
                )
                ORDER BY bi.fecha DESC, bi.hora DESC
                LIMIT 100
            """, [usuario_id])
            
            notificaciones_no_leidas = cursor.fetchall()
            logger.info(f"Notificaciones no leídas encontradas: {len(notificaciones_no_leidas)}")
            
            insertadas = 0
            for row in notificaciones_no_leidas:
                id_pk, novedad = row
                tipo = determinar_tipo_evento(novedad or '')
                
                if tipo in TIPOS_NOTIFICACION:
                    try:
                        cursor.execute("""
                            INSERT INTO notificaciones_leidas 
                            (id_usuario_fk, id_incidente_fk, fecha_lectura) 
                            VALUES (%s, %s, NOW())
                        """, [usuario_id, id_pk])
                        insertadas += 1
                    except Exception as e:
                        # Si hay error de duplicado, lo ignoramos
                        if "Duplicate entry" not in str(e):
                            logger.warning(f"Error insertando notificación {id_pk}: {str(e)}")
            
            connection.commit()
            logger.info(f"Notificaciones insertadas: {insertadas}")
        
        return JsonResponse({'success': True, 'no_leidas': 0, 'insertadas': insertadas})
        
    except Exception as e:
        logger.error(f"Error en api_marcar_todas_leidas: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)