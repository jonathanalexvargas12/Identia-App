# usuarios/views.py (VERSIÓN LIMPIA)
"""
Vistas para autenticación y gestión de usuarios.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from datetime import datetime, date
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


def login_view(request):
    """
    Vista para el formulario de login.
    Autentica usando id_usuario_fk y password contra la base de datos existente.
    """
    # Si ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated:
        messages.info(request, 'Ya tienes una sesión activa')
        return redirect('usuarios:dashboard')
    
    context = {}
    
    if request.method == 'POST':
        # CAMBIO: Usar id_usuario en lugar de cedula
        id_usuario = request.POST.get('id_usuario', '').strip()
        password = request.POST.get('password', '').strip()
        
        logger.info(f"Intento de login recibido - ID Usuario: {id_usuario}")
        
        # Validaciones básicas del formulario
        if not id_usuario:
            messages.error(request, 'El ID de usuario es requerido')
            context['id_usuario'] = id_usuario
            return render(request, 'usuarios/login.html', context)
        
        if not password:
            messages.error(request, 'La contraseña es requerida')
            context['id_usuario'] = id_usuario
            return render(request, 'usuarios/login.html', context)
        
        # CAMBIO: Validar que sea numérico (id_usuario_fk es INT en la BD)
        if not id_usuario.isdigit():
            messages.error(request, 'El ID de usuario debe contener solo números')
            context['id_usuario'] = id_usuario
            return render(request, 'usuarios/login.html', context)
        
        # CAMBIO: Validar rango apropiado para un ID
        try:
            id_num = int(id_usuario)
            if id_num <= 0:
                messages.error(request, 'El ID de usuario debe ser mayor a 0')
                context['id_usuario'] = id_usuario
                return render(request, 'usuarios/login.html', context)
            # Opcional: validar máximo según tu rango de IDs
            if id_num > 99999999:  # 8 dígitos máximo
                messages.error(request, 'ID de usuario demasiado grande')
                context['id_usuario'] = id_usuario
                return render(request, 'usuarios/login.html', context)
        except ValueError:
            messages.error(request, 'ID de usuario inválido')
            context['id_usuario'] = id_usuario
            return render(request, 'usuarios/login.html', context)
        
        # Autenticar usando nuestro backend personalizado
        user = authenticate(request, username=id_usuario, password=password)
        
        if user is not None:
            # Login exitoso
            login(request, user)
            logger.info(f"Login exitoso para ID usuario: {id_usuario}")
            messages.success(request, f'¡Bienvenido/a {user.first_name}!')
            
            # Redirigir según parámetro 'next' o al dashboard
            next_url = request.GET.get('next', '')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            
            return redirect('usuarios:dashboard')
        else:
            # Login fallido (los mensajes de error ya fueron configurados por el backend)
            logger.warning(f"Login fallido para ID usuario: {id_usuario}")
            context['id_usuario'] = id_usuario
            return render(request, 'usuarios/login.html', context)
    
    # GET request - mostrar formulario vacío
    # Incluir parámetro 'next' si está presente
    if 'next' in request.GET:
        context['next'] = request.GET['next']
    
    return render(request, 'usuarios/login.html', context)


@login_required
def get_current_time_view(request):
    """
    Vista para obtener la hora actual del servidor (para AJAX).
    """
    ahora = datetime.now()
    data = {
        'time': ahora.strftime('%H:%M'),
        'date': ahora.strftime('%d/%m/%Y'),
        'datetime': ahora.strftime('%d/%m/Y %H:%M:%S'),
        'timestamp': ahora.timestamp()
    }
    
    return JsonResponse(data)


@login_required
def logout_view(request):
    """
    Vista para cerrar sesión.
    """
    username = request.user.username
    empleado_nombre = request.session.get('empleado_nombres', 'Usuario')
    
    logout(request)
    
    # Limpiar datos de sesión personalizados
    session_keys = ['empleado_id', 'empleado_cedula', 'empleado_nombres', 
                   'empleado_apellidos', 'empleado_correo', 'empleado_estado',
                   'is_authenticated_via_custom']
    
    for key in session_keys:
        if key in request.session:
            del request.session[key]
    
    messages.success(request, f'¡Hasta pronto {empleado_nombre}! Has cerrado sesión exitosamente')
    logger.info(f"Logout exitoso para usuario: {username}")
    
    return redirect('usuarios:login')


# ============================================================================
# NUEVAS VISTAS PARA HOME Y MENÚ LATERAL (AGREGADAS SIN MODIFICAR LO EXISTENTE)
# ============================================================================

@login_required
def home_principal_view(request):
    """
    Home principal del sistema con menú lateral.
    """
    # Obtener datos del empleado desde la sesión
    empleado_data = {
        'id': request.session.get('empleado_id'),
        'nombres': request.session.get('empleado_nombres', 'Usuario'),
        'apellidos': request.session.get('empleado_apellidos', ''),
        'cedula': request.session.get('empleado_cedula', ''),
        'correo': request.session.get('empleado_correo', ''),
        'estado': request.session.get('empleado_estado', ''),
    }
    
    context = {
        'page_title': 'Inicio - Sistema de Gestión',
        'menu_activo': 'inicio',
        'empleado': empleado_data,
        'hoy': date.today(),
        'ahora': datetime.now(),
        'user_ip': request.META.get('REMOTE_ADDR', 'Desconocida'),
    }
    
    return render(request, 'usuarios/home_principal.html', context)


@login_required
def control_acceso_view(request):
    """
    Vista para el módulo de Control de Acceso.
    """
    context = {
        'page_title': 'Control de Acceso',
        'menu_activo': 'control_acceso',
        'hoy': date.today(),
        'ahora': datetime.now(),
    }
    return render(request, 'usuarios/modulos/control_acceso.html', context)


# ============================================================================
# VISTA SIMPLIFICADA DE LISTADO DE TRABAJADORES (SOLO PARA REFERENCIA/REDIRECCIÓN)
# ============================================================================

@login_required
def buscar_trabajadores_view(request):
    """
    Vista redirigida para buscar trabajadores.
    Ahora la gestión completa está en el módulo de reconocimiento.
    """
    from django.db import connection
    from datetime import date
    
    # Obtener parámetro de búsqueda
    search_query = request.GET.get('search', '').strip()
    
    # Mensaje informativo sobre la redirección
    messages.info(request, 
        'La gestión completa de trabajadores ahora se encuentra en el módulo de Reconocimiento Facial. '
        'Redirigiendo...')
    
    # Redirigir al nuevo módulo
    return redirect('reconocimiento:gestion_trabajadores')


@login_required
def seguridad_view(request):
    """
    Vista para el módulo de Seguridad.
    """
    context = {
        'page_title': 'Seguridad',
        'menu_activo': 'seguridad',
        'hoy': date.today(),
        'ahora': datetime.now(),
    }
    return render(request, 'usuarios/seguridad.html', context)

@login_required
def modulos_gestion_view(request):
    """
    Vista para el módulo de Módulos de Gestión.
    """
    context = {
        'page_title': 'Módulos de Gestión',
        'menu_activo': 'seguridad',
        'hoy': date.today(),
        'ahora': datetime.now(),
    }
    return render(request, 'usuarios/modulos_gestion.html', context)


@login_required
def reportes_view(request):
    """
    Vista para el módulo de Reportes.
    """
    context = {
        'page_title': 'Reportes',
        'menu_activo': 'reportes',
        'hoy': date.today(),
        'ahora': datetime.now(),
    }
    return render(request, 'usuarios/modulos/reportes.html', context)


# ============================================================================
# VISTAS EXISTENTES (NO MODIFICADAS)
# ============================================================================

@login_required
def dashboard_view(request):
    """
    Dashboard principal después del login.
    Muestra información del usuario y opciones del sistema.
    """
    # Obtener datos del empleado desde la sesión
    empleado_data = {
        'id': request.session.get('empleado_id'),
        'cedula': request.session.get('empleado_cedula', 'No disponible'),
        'nombres': request.session.get('empleado_nombres', 'Usuario'),
        'apellidos': request.session.get('empleado_apellidos', ''),
        'correo': request.session.get('empleado_correo', ''),
        'estado': request.session.get('empleado_estado', 'Desconocido'),
        'es_administrativo': 'empleado_id' in request.session,
    }
    
    # Obtener información adicional de la base de datos
    from django.db import connection
    
    try:
        with connection.cursor() as cursor:
            # Obtener tipo de personal
            if empleado_data['id']:
                cursor.execute("""
                    SELECT u.tipo_fk, u.area_trabajo, u.rol 
                    FROM usuarios u
                    WHERE u.id_pk = %s
                """, [empleado_data['id']])
                
                resultado = cursor.fetchone()
                if resultado:
                    empleado_data['tipo_personal'] = resultado[0]
                    empleado_data['area_trabajo'] = resultado[1]
                    empleado_data['rol'] = resultado[2]
                
                # Obtener registro de asistencia de hoy
                from datetime import date
                hoy = date.today().isoformat()
                
                cursor.execute("""
                    SELECT 
                        acceso, hora_acceso, 
                        salida, hora_salida,
                        estado_jornada
                    FROM bitacora_asistencia 
                    WHERE id_usuario_fk = %s AND fecha = %s
                    ORDER BY hora_acceso DESC
                    LIMIT 1
                """, [empleado_data['id'], hoy])
                
                asistencia_hoy = cursor.fetchone()
                if asistencia_hoy:
                    empleado_data['asistencia'] = {
                        'acceso': asistencia_hoy[0],
                        'hora_acceso': asistencia_hoy[1],
                        'salida': asistencia_hoy[2],
                        'hora_salida': asistencia_hoy[3],
                        'estado_jornada': asistencia_hoy[4],
                    }
    
    except Exception as e:
        logger.error(f"Error obteniendo datos del dashboard: {str(e)}")
        empleado_data['error_bd'] = "No se pudieron cargar todos los datos"
    
    # Estadísticas para el dashboard
    stats = {}
    try:
        with connection.cursor() as cursor:
            # Total de empleados
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE estado = 'Activo'")
            stats['total_empleados'] = cursor.fetchone()[0]
            
            # Empleados hoy
            from datetime import date
            hoy = date.today().isoformat()
            cursor.execute("""
                SELECT COUNT(DISTINCT id_usuario_fk) 
                FROM bitacora_asistencia 
                WHERE fecha = %s
            """, [hoy])
            stats['empleados_hoy'] = cursor.fetchone()[0]
            
            # Incidentes recientes
            cursor.execute("""
                SELECT COUNT(*) 
                FROM bitacora_incidentes 
                WHERE fecha = %s
            """, [hoy])
            stats['incidentes_hoy'] = cursor.fetchone()[0]
            
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {str(e)}")
        stats = {'error': 'No se pudieron cargar estadísticas'}
    
    context = {
        'empleado': empleado_data,
        'user': request.user,
        'stats': stats,
        'page_title': 'Dashboard Principal',
        'hoy': date.today(),
        'ahora': datetime.now(),
    }
    
    return render(request, 'usuarios/dashboard.html', context)


@login_required
def perfil_view(request):
    """
    Vista para ver y editar el perfil del usuario.
    """
    empleado_id = request.session.get('empleado_id')
    
    if not empleado_id:
        messages.error(request, 'No se encontró información de perfil')
        return redirect('usuarios:dashboard')
    
    from django.db import connection
    
    if request.method == 'POST':
        # Actualizar información del perfil
        try:
            telefono = request.POST.get('telefono', '').strip()
            correo = request.POST.get('correo', '').strip()
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE usuarios 
                    SET numero = %s, correo = %s 
                    WHERE id_pk = %s
                """, [telefono, correo, empleado_id])
                connection.commit()
                
                # Actualizar datos en sesión
                request.session['empleado_correo'] = correo
                
                messages.success(request, 'Perfil actualizado correctamente')
                logger.info(f"Perfil actualizado para empleado ID: {empleado_id}")
                
        except Exception as e:
            messages.error(request, f'Error al actualizar perfil: {str(e)}')
            logger.error(f"Error actualizando perfil: {str(e)}")
    
    # Obtener información actual del empleado
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    u.cedula, u.nombres, u.apellidos, u.direccion_habitacional,
                    u.correo, u.numero, u.estado, u.area_trabajo, u.rol,
                    u.tipo_fk
                FROM usuarios u
                WHERE u.id_pk = %s
            """, [empleado_id])
            
            resultado = cursor.fetchone()
            
            if resultado:
                perfil_data = {
                    'cedula': resultado[0],
                    'nombres': resultado[1],
                    'apellidos': resultado[2],
                    'direccion': resultado[3],
                    'correo': resultado[4],
                    'telefono': resultado[5],
                    'estado': resultado[6],
                    'area_trabajo': resultado[7],
                    'rol': resultado[8],
                    'tipo_personal': resultado[9],
                }
            else:
                messages.error(request, 'No se encontró información del empleado')
                return redirect('usuarios:dashboard')
                
    except Exception as e:
        messages.error(request, f'Error al cargar perfil: {str(e)}')
        logger.error(f"Error cargando perfil: {str(e)}")
        return redirect('usuarios:dashboard')
    
    context = {
        'perfil': perfil_data,
        'page_title': 'Mi Perfil',
        'hoy': date.today(),
        'ahora': datetime.now(),
    }
    
    return render(request, 'usuarios/perfil.html', context)


def home_view(request):
    """
    Vista de la página principal (pública).
    """
    context = {
        'hoy': date.today(),
        'ahora': datetime.now(),
    }
    return render(request, 'usuarios/home.html', context)


def acerca_view(request):
    """
    Vista 'Acerca de' - información del sistema.
    """
    context = {
        'sistema_nombre': 'TerminalApp - Sistema de Gestión Interna',
        'version': '1.0.0',
        'descripcion': 'Sistema de gestión para terminales de transporte con reconocimiento facial',
        'funcionalidades': [
            'Control de acceso con reconocimiento facial',
            'Registro de asistencia automático',
            'Gestión de empleados y horarios',
            'Reportes y estadísticas',
            'Notificaciones en tiempo real',
        ],
        'tecnologias': [
            'Python 3.14',
            'Django 6.0',
            'MariaDB 12.1',
            'OpenCV para reconocimiento facial',
            'HTML5, CSS3, JavaScript',
        ],
        'hoy': date.today(),
        'ahora': datetime.now(),
    }
    
    return render(request, 'usuarios/acerca.html', context)


@login_required
def ayuda_view(request):
    """
    Vista de ayuda para usuarios autenticados.
    """
    context = {
        'hoy': date.today(),
        'ahora': datetime.now(),
    }
    return render(request, 'usuarios/ayuda.html', context)


# ==============================================
# VISTAS DE PRUEBA Y DESARROLLO
# ==============================================

@login_required
def debug_session_view(request):
    """
    Vista de debug para ver información de sesión (solo desarrollo).
    """
    # Cambia esto por tu variable DEBUG real
    DEBUG = True
    
    if not DEBUG:
        messages.error(request, 'Esta vista solo está disponible en modo desarrollo')
        return redirect('usuarios:dashboard')
    
    session_data = {}
    for key, value in request.session.items():
        session_data[key] = str(value)
    
    user_data = {
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'is_staff': request.user.is_staff,
        'is_superuser': request.user.is_superuser,
        'is_active': request.user.is_active,
        'date_joined': request.user.date_joined,
        'last_login': request.user.last_login,
    }
    
    context = {
        'session_data': session_data,
        'user_data': user_data,
        'cookies': request.COOKIES,
        'page_title': 'Debug - Información de Sesión',
        'hoy': date.today(),
        'ahora': datetime.now(),
    }
    
    return render(request, 'usuarios/debug_session.html', context)


# ============================================================================
# CRUD PARA TIPOS DE PERSONAL - MODIFICADO CON BÚSQUEDA MEJORADA
# ============================================================================

@login_required
def gestion_tipos_personal_view(request):
    """
    Vista principal para gestionar tipos de personal (lista y formulario).
    Maneja todas las operaciones CRUD.
    """
    from django.db import connection
    import json
    import re
    
    # Obtener parámetros de búsqueda y acción
    search_query = request.GET.get('search', '').strip()
    accion = request.GET.get('accion', '')
    id_tipo = request.GET.get('id', '')
    
    # Variable para datos del tipo a editar
    tipo_editar = None
    form_data = {}
    
    # ========== MANEJO DE FORMULARIOS POST (Agregar/Editar) ==========
    if request.method == 'POST':
        # Obtener datos del formulario
        nuevo_nombre_raw = request.POST.get('id_nombre_tipo', '').strip()
        accion_post = request.POST.get('accion', '')
        id_tipo_original = request.POST.get('id_tipo_original', '')
        
        # Limpiar el valor recibido (puede venir como JSON desde el datalist)
        nuevo_nombre = nuevo_nombre_raw
        
        # Si el valor parece un objeto JSON/diccionario, extraer solo el nombre
        if nuevo_nombre and (nuevo_nombre.startswith('{') or nuevo_nombre.startswith('[') or 
                           'nombre' in nuevo_nombre.lower() or 'id_nombre_tipo' in nuevo_nombre.lower()):
            try:
                # Reemplazar comillas simples por dobles para JSON válido
                json_str = nuevo_nombre.replace("'", '"')
                # Eliminar espacios extra
                json_str = re.sub(r',\s*"', ',"', json_str)
                
                data = json.loads(json_str)
                
                if isinstance(data, dict):
                    # Buscar el nombre en varias posibles claves
                    for key in ['nombre', 'id_nombre_tipo', 'name', 'tipo', 'value']:
                        if key in data and data[key]:
                            nuevo_nombre = str(data[key]).strip()
                            break
                elif isinstance(data, str):
                    nuevo_nombre = data.strip()
                    
            except json.JSONDecodeError:
                # Si no es JSON válido, intentar extraer texto entre comillas
                match = re.search(r'"nombre"\s*:\s*"([^"]+)"', nuevo_nombre)
                if match:
                    nuevo_nombre = match.group(1)
                else:
                    # Último recurso: eliminar caracteres problemáticos
                    nuevo_nombre = re.sub(r'[{}[\]:,"\'\\]', '', nuevo_nombre).strip()
        
        # Limitar longitud máxima para prevenir errores de base de datos
        if len(nuevo_nombre) > 100:
            nuevo_nombre = nuevo_nombre[:100]
        
        # Validaciones básicas
        if not nuevo_nombre:
            messages.error(request, 'El nombre del tipo es requerido')
            form_data = {'id_nombre_tipo': nuevo_nombre_raw}
            
            if accion_post == 'editar' and id_tipo_original:
                # Usar reverse correctamente para la redirección
                return redirect(f"{reverse('usuarios:gestion_tipos_personal')}?accion=editar&id={id_tipo_original}")
            else:
                return redirect(f"{reverse('usuarios:gestion_tipos_personal')}?accion=agregar")
        
        try:
            if accion_post == 'agregar':
                # Verificar si el tipo ya existe
                with connection.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM tipos_personal WHERE id_nombre_tipo = %s", [nuevo_nombre])
                    if cursor.fetchone()[0] > 0:
                        messages.error(request, f'El tipo "{nuevo_nombre}" ya está registrado')
                        form_data = {'id_nombre_tipo': nuevo_nombre}
                        return redirect(f"{reverse('usuarios:gestion_tipos_personal')}?accion=agregar")
                
                # Insertar nuevo tipo
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO tipos_personal (id_nombre_tipo) VALUES (%s)", [nuevo_nombre])
                    connection.commit()
                    
                messages.success(request, f'Tipo de personal "{nuevo_nombre}" agregado exitosamente')
                return redirect('usuarios:gestion_tipos_personal')
            
            elif accion_post == 'editar' and id_tipo_original:
                # Verificar que el tipo original exista
                with connection.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM tipos_personal WHERE id_nombre_tipo = %s", [id_tipo_original])
                    if cursor.fetchone()[0] == 0:
                        messages.error(request, f'El tipo original "{id_tipo_original}" no existe')
                        return redirect('usuarios:gestion_tipos_personal')
                
                # Si el nombre cambió, verificar que no exista ya
                if nuevo_nombre != id_tipo_original:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT COUNT(*) FROM tipos_personal WHERE id_nombre_tipo = %s", [nuevo_nombre])
                        if cursor.fetchone()[0] > 0:
                            messages.error(request, f'El tipo "{nuevo_nombre}" ya existe')
                            return redirect(f"{reverse('usuarios:gestion_tipos_personal')}?accion=editar&id={id_tipo_original}")
                
                # Actualizar tipo en todas las tablas relacionadas
                with connection.cursor() as cursor:
                    # Actualizar usuarios
                    cursor.execute("UPDATE usuarios SET tipo_fk = %s WHERE tipo_fk = %s", 
                                 [nuevo_nombre, id_tipo_original])
                    # Actualizar horarios
                    cursor.execute("UPDATE horarios_jornada SET tipo_fk = %s WHERE tipo_fk = %s", 
                                 [nuevo_nombre, id_tipo_original])
                    # Actualizar tipo principal
                    cursor.execute("UPDATE tipos_personal SET id_nombre_tipo = %s WHERE id_nombre_tipo = %s", 
                                 [nuevo_nombre, id_tipo_original])
                    connection.commit()
                
                messages.success(request, f'Tipo actualizado: "{id_tipo_original}" → "{nuevo_nombre}"')
                return redirect('usuarios:gestion_tipos_personal')
                
        except Exception as e:
            error_msg = f'Error: {str(e)}'
            if "1406" in str(e) or "Data too long" in str(e):
                error_msg = 'Error: El nombre es demasiado largo para la base de datos'
            elif "1452" in str(e):
                error_msg = 'Error de referencia: El tipo no existe o tiene formato incorrecto'
            
            messages.error(request, error_msg)
            
            if accion_post == 'editar' and id_tipo_original:
                return redirect(f"{reverse('usuarios:gestion_tipos_personal')}?accion=editar&id={id_tipo_original}")
            else:
                return redirect(f"{reverse('usuarios:gestion_tipos_personal')}?accion=agregar")
    
    # ========== MANEJO DE ELIMINACIÓN ==========
    elif request.method == 'GET' and accion == 'eliminar' and id_tipo:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM usuarios WHERE tipo_fk = %s", [id_tipo])
                tiene_usuarios = cursor.fetchone()[0] > 0
                
                cursor.execute("SELECT COUNT(*) FROM horarios_jornada WHERE tipo_fk = %s", [id_tipo])
                tiene_horarios = cursor.fetchone()[0] > 0
                
                if tiene_usuarios or tiene_horarios:
                    messages.warning(request, 
                        f'No se puede eliminar el tipo "{id_tipo}" porque tiene registros relacionados.')
                else:
                    cursor.execute("DELETE FROM tipos_personal WHERE id_nombre_tipo = %s", [id_tipo])
                    connection.commit()
                    messages.success(request, f'Tipo "{id_tipo}" eliminado exitosamente')
                    
        except Exception as e:
            messages.error(request, f'Error al eliminar: {str(e)}')
        
        return redirect('usuarios:gestion_tipos_personal')
    
    # ========== CARGAR DATOS PARA EDICIÓN ==========
    if accion == 'editar' and id_tipo:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_nombre_tipo FROM tipos_personal WHERE id_nombre_tipo = %s", [id_tipo])
                resultado = cursor.fetchone()
                if resultado:
                    tipo_editar = {'id_nombre_tipo': resultado[0]}
                else:
                    messages.error(request, f'Tipo "{id_tipo}" no encontrado')
                    return redirect('usuarios:gestion_tipos_personal')
        except Exception as e:
            messages.error(request, f'Error al cargar datos: {str(e)}')
    
    # ========== OBTENER LISTA DE TIPOS ==========
    query = "SELECT id_nombre_tipo FROM tipos_personal"
    params = []
    
    if search_query and accion not in ['agregar', 'editar', 'confirmar_eliminar']:
        query += " WHERE id_nombre_tipo LIKE %s"
        params = [f"%{search_query}%"]
    
    query += " ORDER BY id_nombre_tipo"
    
    tipos_personal = []
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            for row in cursor.fetchall():
                tipo_nombre = row[0]
                
                cursor.execute("SELECT COUNT(*) FROM usuarios WHERE tipo_fk = %s", [tipo_nombre])
                total_usuarios = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM horarios_jornada WHERE tipo_fk = %s", [tipo_nombre])
                total_horarios = cursor.fetchone()[0]
                
                tipos_personal.append({
                    'id_nombre_tipo': tipo_nombre,
                    'total_usuarios': total_usuarios,
                    'total_horarios': total_horarios
                })
    except Exception as e:
        logger.error(f"Error obteniendo tipos: {str(e)}")
        tipos_personal = []
    
    # ========== OBTENER TODOS LOS TIPOS PARA EL DATALIST ==========
    # Para evitar problemas con JSON en el datalist, solo enviamos los nombres
    todos_los_tipos = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_nombre_tipo FROM tipos_personal ORDER BY id_nombre_tipo")
            todos_los_tipos = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Error obteniendo todos los tipos: {str(e)}")
        todos_los_tipos = []
    
    context = {
        'page_title': 'Gestión de Tipos de Personal',
        'menu_activo': 'seguridad',
        'tipos_personal': tipos_personal,
        'todos_los_tipos': todos_los_tipos,  # Solo nombres, no objetos
        'search_query': search_query,
        'tipo_editar': tipo_editar,
        'form_data': form_data,
        'hoy': date.today(),
        'ahora': datetime.now(),
        'accion_actual': accion,
        'id_tipo_actual': id_tipo,
        'acciones_formulario': ['agregar', 'editar', 'confirmar_eliminar']
    }
    
    return render(request, 'usuarios/gestion_tipos_personal.html', context)


# ============================================================================
# CRUD PARA HORARIOS DE JORNADA
# ============================================================================

@login_required
def gestion_horarios_view(request):
    """
    Vista principal para gestionar horarios de jornada.
    Maneja CRUD completo para la tabla horarios_jornada.
    """
    from django.db import connection
    import json
    import re
    
    # Obtener parámetros
    search_query = request.GET.get('search', '').strip()
    accion = request.GET.get('accion', '')
    id_horario = request.GET.get('id', '')
    
    # Variables para formulario
    horario_editar = None
    form_data = {}
    tipos_personal_lista = []
    
    # ========== OBTENER LISTA DE TIPOS DE PERSONAL ==========
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_nombre_tipo FROM tipos_personal ORDER BY id_nombre_tipo")
            tipos_personal_lista = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Error obteniendo tipos de personal: {str(e)}")
        tipos_personal_lista = []
    
    # ========== MANEJO DE FORMULARIOS POST (Agregar/Editar) ==========
    if request.method == 'POST':
        # Obtener datos del formulario
        accion_post = request.POST.get('accion', '')
        id_horario_original = request.POST.get('id_horario_original', '')
        
        # Procesar datos del formulario
        tipo_personal_raw = request.POST.get('tipo_fk', '').strip()
        fecha_raw = request.POST.get('fecha', '').strip()
        hora_entrada_raw = request.POST.get('hora_entrada', '').strip()
        hora_salida_raw = request.POST.get('hora_salida', '').strip()
        tolerancia_entrada_raw = request.POST.get('tolerancia_entrada', '').strip()
        tolerancia_salida_raw = request.POST.get('tolerancia_salida', '').strip()
        
        # Procesar tipo_personal (puede venir como JSON del datalist)
        tipo_personal = tipo_personal_raw
        if tipo_personal and (tipo_personal.startswith('{') or 'nombre' in tipo_personal.lower()):
            try:
                json_str = tipo_personal.replace("'", '"')
                data = json.loads(json_str)
                if isinstance(data, dict):
                    for key in ['nombre', 'id_nombre_tipo', 'tipo', 'value']:
                        if key in data and data[key]:
                            tipo_personal = str(data[key]).strip()
                            break
            except json.JSONDecodeError:
                match = re.search(r'"nombre"\s*:\s*"([^"]+)"', tipo_personal)
                if match:
                    tipo_personal = match.group(1)
                else:
                    tipo_personal = re.sub(r'[{}[\]:,"\'\\]', '', tipo_personal).strip()
        
        # Validar tipo de personal
        if not tipo_personal or tipo_personal not in tipos_personal_lista:
            messages.error(request, 'Tipo de personal no válido o no seleccionado')
            form_data = {
                'tipo_fk': tipo_personal_raw,
                'fecha': fecha_raw,
                'hora_entrada': hora_entrada_raw,
                'hora_salida': hora_salida_raw,
                'tolerancia_entrada': tolerancia_entrada_raw,
                'tolerancia_salida': tolerancia_salida_raw,
            }
            if accion_post == 'editar' and id_horario_original:
                return redirect(f"{reverse('usuarios:gestion_horarios')}?accion=editar&id={id_horario_original}")
            return redirect(f"{reverse('usuarios:gestion_horarios')}?accion=agregar")
        
        # Convertir valores NULL/empty
        fecha = fecha_raw if fecha_raw else None
        hora_entrada = hora_entrada_raw if hora_entrada_raw else None
        hora_salida = hora_salida_raw if hora_salida_raw else None
        tolerancia_entrada = tolerancia_entrada_raw if tolerancia_entrada_raw else None
        tolerancia_salida = tolerancia_salida_raw if tolerancia_salida_raw else None
        
        try:
            if accion_post == 'agregar':
                # Verificar si ya existe un horario para este tipo en esta fecha
                if fecha:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            SELECT COUNT(*) FROM horarios_jornada 
                            WHERE tipo_fk = %s AND fecha = %s
                        """, [tipo_personal, fecha])
                        if cursor.fetchone()[0] > 0:
                            messages.error(request, f'Ya existe un horario para {tipo_personal} en la fecha {fecha}')
                            form_data = {
                                'tipo_fk': tipo_personal_raw,
                                'fecha': fecha_raw,
                                'hora_entrada': hora_entrada_raw,
                                'hora_salida': hora_salida_raw,
                                'tolerancia_entrada': tolerancia_entrada_raw,
                                'tolerancia_salida': tolerancia_salida_raw,
                            }
                            return redirect(f"{reverse('usuarios:gestion_horarios')}?accion=agregar")
                
                # Insertar nuevo horario
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO horarios_jornada 
                        (tipo_fk, fecha, hora_entrada, tolerancia_entrada, 
                         hora_salida, tolerancia_salida) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, [tipo_personal, fecha, hora_entrada, tolerancia_entrada, 
                          hora_salida, tolerancia_salida])
                    connection.commit()
                
                messages.success(request, 'Horario agregado exitosamente')
                return redirect('usuarios:gestion_horarios')
            
            elif accion_post == 'editar' and id_horario_original:
                try:
                    id_horario_int = int(id_horario_original)
                except ValueError:
                    messages.error(request, 'ID de horario inválido')
                    return redirect('usuarios:gestion_horarios')
                
                # Verificar si existe el horario
                with connection.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM horarios_jornada WHERE id_pk = %s", 
                                 [id_horario_int])
                    if cursor.fetchone()[0] == 0:
                        messages.error(request, 'El horario no existe')
                        return redirect('usuarios:gestion_horarios')
                
                # Verificar duplicado (si cambió tipo o fecha)
                if fecha:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            SELECT COUNT(*) FROM horarios_jornada 
                            WHERE tipo_fk = %s AND fecha = %s AND id_pk != %s
                        """, [tipo_personal, fecha, id_horario_int])
                        if cursor.fetchone()[0] > 0:
                            messages.error(request, f'Ya existe otro horario para {tipo_personal} en la fecha {fecha}')
                            return redirect(f"{reverse('usuarios:gestion_horarios')}?accion=editar&id={id_horario_original}")
                
                # Actualizar horario
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE horarios_jornada 
                        SET tipo_fk = %s, 
                            fecha = %s, 
                            hora_entrada = %s, 
                            tolerancia_entrada = %s,
                            hora_salida = %s, 
                            tolerancia_salida = %s
                        WHERE id_pk = %s
                    """, [tipo_personal, fecha, hora_entrada, tolerancia_entrada, 
                          hora_salida, tolerancia_salida, id_horario_int])
                    connection.commit()
                
                messages.success(request, 'Horario actualizado exitosamente')
                return redirect('usuarios:gestion_horarios')
                
        except Exception as e:
            error_msg = f'Error: {str(e)}'
            if "1452" in str(e):
                error_msg = 'Error: El tipo de personal seleccionado no existe'
            
            messages.error(request, error_msg)
            
            if accion_post == 'editar' and id_horario_original:
                return redirect(f"{reverse('usuarios:gestion_horarios')}?accion=editar&id={id_horario_original}")
            else:
                return redirect(f"{reverse('usuarios:gestion_horarios')}?accion=agregar")
    
    # ========== MANEJO DE ELIMINACIÓN ==========
    elif request.method == 'GET' and accion == 'eliminar' and id_horario:
        try:
            id_horario_int = int(id_horario)
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM horarios_jornada WHERE id_pk = %s", [id_horario_int])
                connection.commit()
                messages.success(request, 'Horario eliminado exitosamente')
        except ValueError:
            messages.error(request, 'ID de horario inválido')
        except Exception as e:
            messages.error(request, f'Error al eliminar: {str(e)}')
        
        return redirect('usuarios:gestion_horarios')
    
    # ========== CARGAR DATOS PARA EDICIÓN ==========
    if accion == 'editar' and id_horario:
        try:
            id_horario_int = int(id_horario)
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id_pk, tipo_fk, fecha, hora_entrada, tolerancia_entrada,
                           hora_salida, tolerancia_salida
                    FROM horarios_jornada WHERE id_pk = %s
                """, [id_horario_int])
                
                resultado = cursor.fetchone()
                if resultado:
                    horario_editar = {
                        'id_pk': resultado[0],
                        'tipo_fk': resultado[1],
                        'fecha': resultado[2],
                        'hora_entrada': resultado[3],
                        'tolerancia_entrada': resultado[4],
                        'hora_salida': resultado[5],
                        'tolerancia_salida': resultado[6],
                    }
                else:
                    messages.error(request, 'Horario no encontrado')
                    return redirect('usuarios:gestion_horarios')
        except ValueError:
            messages.error(request, 'ID de horario inválido')
            return redirect('usuarios:gestion_horarios')
        except Exception as e:
            messages.error(request, f'Error al cargar datos: {str(e)}')
            return redirect('usuarios:gestion_horarios')
    
    # ========== OBTENER LISTA DE HORARIOS ==========
    query = """
        SELECT h.id_pk, h.tipo_fk, h.fecha, h.hora_entrada, h.tolerancia_entrada,
               h.hora_salida, h.tolerancia_salida,
               COUNT(u.id_pk) as total_usuarios
        FROM horarios_jornada h
        LEFT JOIN usuarios u ON h.tipo_fk = u.tipo_fk
    """
    params = []
    
    # Aplicar búsqueda si existe
    if search_query:
        query += " WHERE h.tipo_fk LIKE %s"
        params = [f"%{search_query}%"]
    
    query += " GROUP BY h.id_pk, h.tipo_fk, h.fecha, h.hora_entrada, h.tolerancia_entrada, h.hora_salida, h.tolerancia_salida"
    query += " ORDER BY h.tipo_fk, COALESCE(h.fecha, '1900-01-01'), h.hora_entrada"
    
    horarios_lista = []
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            for row in cursor.fetchall():
                horarios_lista.append({
                    'id_pk': row[0],
                    'tipo_fk': row[1],
                    'fecha': row[2],
                    'hora_entrada': row[3],
                    'tolerancia_entrada': row[4],
                    'hora_salida': row[5],
                    'tolerancia_salida': row[6],
                    'total_usuarios': row[7],
                })
    except Exception as e:
        logger.error(f"Error obteniendo horarios: {str(e)}")
        horarios_lista = []
    
    context = {
        'page_title': 'Gestión de Horarios de Jornada',
        'menu_activo': 'seguridad',
        'horarios_lista': horarios_lista,
        'tipos_personal_lista': tipos_personal_lista,
        'search_query': search_query,
        'horario_editar': horario_editar,
        'form_data': form_data,
        'hoy': date.today(),
        'ahora': datetime.now(),
        'accion_actual': accion,
        'id_horario_actual': id_horario,
        'acciones_formulario': ['agregar', 'editar', 'confirmar_eliminar']
    }
    
    return render(request, 'usuarios/gestion_horarios.html', context)


@login_required
def test_auth_view(request):
    """
    Vista para probar la autenticación (solo desarrollo).
    """
    # Cambia esto por tu variable DEBUG real
    DEBUG = True
    
    if not DEBUG:
        messages.error(request, 'Esta vista solo está disponible en modo desarrollo')
        return redirect('usuarios:dashboard')
    
    from django.db import connection
    
    test_data = {
        'user_authenticated': request.user.is_authenticated,
        'username': request.user.username,
        'session_keys': list(request.session.keys()),
    }
    
    # Probar conexión a BD para autenticación
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            test_data['total_usuarios'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM usuarios_administrativos")
            test_data['total_administrativos'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT id_usuario_fk, password FROM usuarios_administrativos LIMIT 5")
            test_data['administrativos_ejemplo'] = cursor.fetchall()
    
    except Exception as e:
        test_data['bd_error'] = str(e)
    
    context = {
        'test_data': test_data,
        'page_title': 'Prueba de Autenticación',
        'hoy': date.today(),
        'ahora': datetime.now(),
    }
    
    return render(request, 'usuarios/test_auth.html', context)


# ==============================================
# MANEJO DE ERRORES PERSONALIZADOS
# ==============================================

def handler404(request, exception):
    """
    Vista personalizada para error 404.
    """
    logger.warning(f"Página no encontrada: {request.path}")
    context = {
        'error_code': '404',
        'error_message': 'Página no encontrada',
        'request_path': request.path,
        'hoy': date.today(),
        'ahora': datetime.now(),
    }
    return render(request, 'usuarios/error.html', context, status=404)


def handler500(request):
    """
    Vista personalizada para error 500.
    """
    logger.error(f"Error interno del servidor: {request.path}")
    context = {
        'error_code': '500',
        'error_message': 'Error interno del servidor',
        'hoy': date.today(),
        'ahora': datetime.now(),
    }
    return render(request, 'usuarios/error.html', context, status=500)


def handler403(request, exception):
    """
    Vista personalizada para error 403 (permiso denegado).
    """
    logger.warning(f"Acceso denegado: {request.path}")
    context = {
        'error_code': '403',
        'error_message': 'Acceso denegado',
        'hoy': date.today(),
        'ahora': datetime.now(),
    }
    return render(request, 'usuarios/error.html', context, status=403)


def handler400(request, exception):
    """
    Vista personalizada para error 400 (solicitud incorrecta).
    """
    logger.warning(f"Solicitud incorrecta: {request.path}")
    context = {
        'error_code': '400',
        'error_message': 'Solicitud incorrecta',
        'hoy': date.today(),
        'ahora': datetime.now(),
    }
    return render(request, 'usuarios/error.html', context, status=400)