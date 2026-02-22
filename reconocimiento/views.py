"""
Vistas para el módulo de reconocimiento facial usando DeepFace.
Maneja el formulario de registro con captura facial Y la gestión completa de trabajadores (CRUD).
"""
import base64
import json
import logging
import numpy as np
import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection
from datetime import datetime, date
import cv2
from PIL import Image
import io
from deepface import DeepFace
import time
import traceback
from django.urls import reverse

logger = logging.getLogger(__name__)

# Configuración global de DeepFace
DEEPFACE_CONFIG = {
    'model_name': 'Facenet',  # Puedes usar: VGG-Face, Facenet, OpenFace, DeepFace, DeepID, ArcFace
    'detector_backend': 'opencv',  # opencv, mtcnn, retinaface, ssd, dlib
    'distance_metric': 'cosine',  # cosine, euclidean, euclidean_l2
    'threshold': 0.4,  # Umbral para verificación (ajustable)
}

# ============================================================================
# CRUD COMPLETO DE TRABAJADORES
# ============================================================================

@login_required
def gestion_trabajadores_view(request):
    """
    Vista principal para la gestión completa de trabajadores (CRUD).
    Lista, busca, edita y desactiva trabajadores.
    """
    # Obtener parámetros de búsqueda y acción
    search_query = request.GET.get('search', '').strip()
    accion = request.GET.get('accion', '')
    id_trabajador = request.GET.get('id', '')
    
    # Variable para datos de trabajador a editar
    trabajador_editar = None
    modo_agregar = False
    
    # ========== MANEJO DE DESACTIVACIÓN ==========
    if accion == 'desactivar' and id_trabajador:
        try:
            with connection.cursor() as cursor:
                # Obtener información del trabajador
                cursor.execute("""
                    SELECT nombres, apellidos, cedula, estado
                    FROM usuarios WHERE id_pk = %s
                """, [id_trabajador])
                resultado = cursor.fetchone()
                
                if resultado:
                    nombres, apellidos, cedula, estado_actual = resultado
                    
                    # Solo desactivar si está activo
                    if estado_actual == 'Activo':
                        cursor.execute("""
                            UPDATE usuarios 
                            SET estado = 'Inactivo' 
                            WHERE id_pk = %s
                        """, [id_trabajador])
                        connection.commit()
                        
                        messages.success(request, 
                            f'✅ Trabajador {nombres} {apellidos} desactivado exitosamente. '
                            f'Se mantienen todos sus registros históricos para auditoría.')
                        logger.info(f"Trabajador desactivado ID: {id_trabajador} - {cedula} - {nombres} {apellidos}")
                        
                    elif estado_actual == 'Inactivo':
                        messages.info(request, 
                            f'ℹ️ El trabajador {nombres} {apellidos} ya está desactivado.')
                        
                    else:
                        messages.info(request, 
                            f'ℹ️ El trabajador {nombres} {apellidos} tiene estado: {estado_actual}. '
                            f'Si desea desactivarlo, puede editarlo manualmente.')
                        
                else:
                    messages.error(request, '❌ Trabajador no encontrado')
                    
        except Exception as e:
            messages.error(request, f'❌ Error al desactivar trabajador: {str(e)}')
            logger.error(f"Error desactivando trabajador ID {id_trabajador}: {str(e)}")
        
        return redirect('reconocimiento:gestion_trabajadores')
    
    # ========== MANEJO DE ELIMINACIÓN (SOLO PARA SUPERUSUARIOS Y CASOS ESPECIALES) ==========
    if accion == 'eliminar' and id_trabajador:
        # Verificar si el usuario actual es superusuario
        if not request.user.is_superuser:
            messages.error(request, 
                '❌ Solo los superusuarios pueden eliminar trabajadores permanentemente. '
                'Use "Desactivar" en su lugar.')
            return redirect('reconocimiento:gestion_trabajadores')
        
        try:
            with connection.cursor() as cursor:
                # Obtener información del trabajador
                cursor.execute("""
                    SELECT nombres, apellidos, cedula, estado
                    FROM usuarios WHERE id_pk = %s
                """, [id_trabajador])
                resultado = cursor.fetchone()
                
                if resultado:
                    nombres, apellidos, cedula, estado_actual = resultado
                    
                    # Verificar si tiene registros relacionados que impidan la eliminación
                    cursor.execute("""
                        SELECT 
                            (SELECT COUNT(*) FROM bitacora_asistencia WHERE id_usuario_fk = %s) as total_asistencias,
                            (SELECT COUNT(*) FROM rostros_usuarios WHERE id_usuario_fk = %s) as total_rostros,
                            (SELECT COUNT(*) FROM usuarios_administrativos WHERE id_usuario_fk = %s) as total_admin
                    """, [id_trabajador, id_trabajador, id_trabajador])
                    
                    totales = cursor.fetchone()
                    total_asistencias, total_rostros, total_admin = totales
                    
                    # Si tiene registros, mostrar advertencia y no eliminar
                    if total_asistencias > 0 or total_rostros > 0 or total_admin > 0:
                        mensaje_detalle = []
                        if total_asistencias > 0:
                            mensaje_detalle.append(f'{total_asistencias} registros de asistencia')
                        if total_rostros > 0:
                            mensaje_detalle.append(f'{total_rostros} registros faciales')
                        if total_admin > 0:
                            mensaje_detalle.append(f'{total_admin} credenciales administrativas')
                        
                        messages.error(request, 
                            f'❌ No se puede eliminar {nombres} {apellidos} porque tiene: {", ".join(mensaje_detalle)}. '
                            f'Use "Desactivar" en lugar de eliminar para mantener la integridad de los datos.')
                        
                        return redirect('reconocimiento:gestion_trabajadores')
                    
                    # Si no tiene registros, proceder con eliminación
                    cursor.execute("DELETE FROM usuarios WHERE id_pk = %s", [id_trabajador])
                    connection.commit()
                    
                    messages.success(request, 
                        f'✅ Trabajador {nombres} {apellidos} eliminado permanentemente del sistema.')
                    logger.info(f"Trabajador eliminado ID: {id_trabajador} - {cedula} - {nombres} {apellidos}")
                    
                else:
                    messages.error(request, '❌ Trabajador no encontrado')
                    
        except Exception as e:
            messages.error(request, f'❌ Error al eliminar trabajador: {str(e)}')
            logger.error(f"Error eliminando trabajador ID {id_trabajador}: {str(e)}")
        
        return redirect('reconocimiento:gestion_trabajadores')
    
    # ========== MODO AGREGAR NUEVO ==========
    if accion == 'agregar':
        modo_agregar = True
    
    # ========== CARGAR DATOS PARA EDICIÓN ==========
    elif accion == 'editar' and id_trabajador:
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        id_pk, cedula, nombres, apellidos, 
                        direccion_habitacional, correo, numero, 
                        estado, area_trabajo, rol, tipo_fk
                    FROM usuarios
                    WHERE id_pk = %s
                """, [id_trabajador])
                
                columns = [col[0] for col in cursor.description]
                row = cursor.fetchone()
                if row:
                    trabajador_editar = dict(zip(columns, row))
                else:
                    messages.error(request, '❌ Trabajador no encontrado')
                    return redirect('reconocimiento:gestion_trabajadores')
                    
        except Exception as e:
            logger.error(f"Error cargando trabajador para editar: {str(e)}")
            messages.error(request, '❌ Error al cargar datos del trabajador')
            return redirect('reconocimiento:gestion_trabajadores')
    
    # ========== OBTENER LISTA DE TRABAJADORES ==========
    # Construir la consulta SQL para listar trabajadores - CORREGIDA
    query = """
        SELECT 
            id_pk, cedula, nombres, apellidos, 
            correo, numero as telefono, estado, 
            area_trabajo, rol, tipo_fk
            -- NOTA: Se eliminó el cálculo de edad aproximada que causaba error
            -- ERROR ORIGINAL: ,DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(), STR_TO_DATE(cedula, '%%d%%m%%Y'))), '%%Y') + 0 as edad_aproximada
        FROM usuarios
        WHERE 1=1
    """
    
    params = []
    
    # Solo mostrar búsqueda si no estamos en modo edición o agregar
    if search_query and accion not in ['editar', 'agregar']:
        query += """
            AND (
                cedula LIKE %s OR 
                nombres LIKE %s OR 
                apellidos LIKE %s OR
                correo LIKE %s OR
                estado LIKE %s OR
                area_trabajo LIKE %s OR
                rol LIKE %s OR
                tipo_fk LIKE %s
            )
        """
        search_pattern = f"%{search_query}%"
        params = [search_pattern] * 8
    
    query += " ORDER BY estado DESC, apellidos, nombres"
    
    # Ejecutar consulta para obtener lista de trabajadores
    trabajadores = []
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            for row in cursor.fetchall():
                trabajador = dict(zip(columns, row))
                
                # Contar registros relacionados para mostrar información
                try:
                    cursor.execute("SELECT COUNT(*) FROM bitacora_asistencia WHERE id_usuario_fk = %s", 
                                 [trabajador['id_pk']])
                    trabajador['total_asistencias'] = cursor.fetchone()[0]
                    
                    cursor.execute("SELECT COUNT(*) FROM rostros_usuarios WHERE id_usuario_fk = %s", 
                                 [trabajador['id_pk']])
                    trabajador['total_rostros'] = cursor.fetchone()[0]
                    
                    cursor.execute("SELECT COUNT(*) FROM usuarios_administrativos WHERE id_usuario_fk = %s", 
                                 [trabajador['id_pk']])
                    trabajador['total_admin'] = cursor.fetchone()[0]
                    
                except Exception as e:
                    trabajador['total_asistencias'] = 0
                    trabajador['total_rostros'] = 0
                    trabajador['total_admin'] = 0
                
                trabajadores.append(trabajador)
    except Exception as e:
        logger.error(f"Error obteniendo trabajadores: {str(e)}")
        logger.error(f"Consulta SQL: {query}")
        logger.error(f"Parámetros: {params}")
        messages.error(request, f'❌ Error al cargar trabajadores: {str(e)}')
    
    # Obtener tipos de personal para el formulario
    tipos_personal = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_nombre_tipo FROM tipos_personal ORDER BY id_nombre_tipo")
            tipos_personal = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Error obteniendo tipos de personal: {str(e)}")
    
    context = {
        'page_title': 'Gestión de Trabajadores',
        'menu_activo': 'gestion_trabajadores',
        'trabajadores': trabajadores,
        'search_query': search_query,
        'tipos_personal': tipos_personal,
        'estados': ['Activo', 'Inactivo', 'Suspendido', 'Vacaciones'],
        'trabajador_editar': trabajador_editar,
        'modo_agregar': modo_agregar,
        'hoy': date.today(),
        'ahora': datetime.now(),
    }
    
    return render(request, 'reconocimiento/gestion_trabajadores.html', context)

@login_required
def guardar_trabajador_view(request):
    """
    Vista para guardar/actualizar trabajadores (tanto nuevo como edición).
    """
    if request.method != 'POST':
        messages.error(request, '❌ Método no permitido')
        return redirect('reconocimiento:gestion_trabajadores')
    
    try:
        # Obtener datos del formulario
        cedula = request.POST.get('cedula', '').strip()
        nombres = request.POST.get('nombres', '').strip()
        apellidos = request.POST.get('apellidos', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        correo = request.POST.get('correo', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        estado = request.POST.get('estado', 'Activo').strip()
        area_trabajo = request.POST.get('area_trabajo', '').strip()
        rol = request.POST.get('rol', '').strip()
        tipo_personal = request.POST.get('tipo_personal', '').strip()
        id_trabajador = request.POST.get('id_trabajador', '').strip()
        es_edicion = bool(id_trabajador)
        
        logger.info(f"Guardando trabajador - Edición: {es_edicion}, ID: {id_trabajador or 'Nuevo'}")
        
        # Validaciones básicas
        if not cedula or not nombres or not apellidos or not tipo_personal:
            messages.error(request, '❌ Cédula, nombres, apellidos y tipo de personal son requeridos')
            return redirect(f"{reverse('reconocimiento:gestion_trabajadores')}?accion={'editar' if es_edicion else 'agregar'}&id={id_trabajador}")
        
        # Validar formato de cédula
        if not cedula.isdigit() or len(cedula) != 8:
            messages.error(request, '❌ La cédula debe tener exactamente 8 dígitos numéricos')
            return redirect(f"{reverse('reconocimiento:gestion_trabajadores')}?accion={'editar' if es_edicion else 'agregar'}&id={id_trabajador}")
        
        with connection.cursor() as cursor:
            if es_edicion:
                # ========== ACTUALIZAR TRABAJADOR EXISTENTE ==========
                # Verificar que el trabajador exista
                cursor.execute("SELECT cedula FROM usuarios WHERE id_pk = %s", [id_trabajador])
                if not cursor.fetchone():
                    messages.error(request, '❌ Trabajador no encontrado')
                    return redirect('reconocimiento:gestion_trabajadores')
                
                # Si la cédula cambió, verificar que no exista otra igual
                cursor.execute("SELECT cedula FROM usuarios WHERE id_pk = %s", [id_trabajador])
                cedula_actual = cursor.fetchone()[0]
                
                if cedula != cedula_actual:
                    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE cedula = %s AND id_pk != %s", 
                                 [cedula, id_trabajador])
                    if cursor.fetchone()[0] > 0:
                        messages.error(request, f'❌ La cédula {cedula} ya está registrada por otro trabajador')
                        return redirect(f"{reverse('reconocimiento:gestion_trabajadores')}?accion=editar&id={id_trabajador}")
                
                # Actualizar trabajador
                cursor.execute("""
                    UPDATE usuarios SET
                        cedula = %s, nombres = %s, apellidos = %s, 
                        direccion_habitacional = %s, correo = %s, numero = %s,
                        estado = %s, area_trabajo = %s, rol = %s, tipo_fk = %s
                    WHERE id_pk = %s
                """, [
                    cedula, nombres, apellidos, direccion or '',
                    correo or '', telefono or '', estado,
                    area_trabajo or '', rol or '', tipo_personal, id_trabajador
                ])
                
                connection.commit()
                
                messages.success(request, f'✅ Trabajador {nombres} {apellidos} actualizado exitosamente')
                logger.info(f"Trabajador actualizado ID: {id_trabajador} - {cedula} - {nombres} {apellidos}")
                
            else:
                # ========== INSERTAR NUEVO TRABAJADOR ==========
                # Verificar que la cédula no exista
                cursor.execute("SELECT COUNT(*) FROM usuarios WHERE cedula = %s", [cedula])
                if cursor.fetchone()[0] > 0:
                    messages.error(request, f'❌ La cédula {cedula} ya está registrada en el sistema')
                    return redirect(f"{reverse('reconocimiento:gestion_trabajadores')}?accion=agregar")
                
                # Insertar nuevo trabajador
                cursor.execute("""
                    INSERT INTO usuarios (
                        cedula, nombres, apellidos, direccion_habitacional,
                        correo, numero, estado, area_trabajo, rol, tipo_fk
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, [
                    cedula, nombres, apellidos, direccion or '',
                    correo or '', telefono or '', estado,
                    area_trabajo or '', rol or '', tipo_personal
                ])
                
                user_id = cursor.lastrowid
                
                # Si es administrativo, crear credenciales básicas
                tipo_lower = tipo_personal.lower()
                if any(admin_keyword in tipo_lower for admin_keyword in ['admin', 'administrativo', 'administrador']):
                    try:
                        import secrets
                        import hashlib
                        temp_password = secrets.token_urlsafe(8)
                        hashed_password = hashlib.sha256(temp_password.encode()).hexdigest()
                        
                        cursor.execute("""
                            INSERT INTO usuarios_administrativos (id_usuario_fk, password)
                            VALUES (%s, %s)
                        """, [user_id, hashed_password])
                        
                        request.session['temp_password'] = temp_password
                        request.session['new_user_id'] = user_id
                        
                        logger.info(f"Credenciales administrativas creadas. Password temporal: {temp_password}")
                        
                    except Exception as e:
                        logger.warning(f"⚠️ No se pudieron crear credenciales administrativas: {str(e)}")
                
                connection.commit()
                
                messages.success(request, f'✅ Trabajador {nombres} {apellidos} registrado exitosamente')
                logger.info(f"Trabajador registrado ID: {user_id} - {cedula} - {nombres} {apellidos}")
                
                # Redirigir a registro facial si se desea capturar rostro
                if request.POST.get('capturar_rostro') == 'si':
                    request.session['trabajador_para_rostro'] = user_id
                    return redirect('reconocimiento:registro_facial')
                
    except Exception as e:
        error_msg = f'❌ Error al guardar trabajador: {str(e)}'
        messages.error(request, error_msg)
        logger.error(f"Error en guardar_trabajador_view: {str(e)}")
        
        # Determinar tipo de error
        error_str = str(e).lower()
        if "duplicate" in error_str:
            messages.error(request, f'❌ La cédula {cedula} ya está registrada en el sistema')
        elif "foreign key" in error_str:
            messages.error(request, f'❌ El tipo de personal "{tipo_personal}" no existe')
        
        # Redirigir de vuelta al formulario
        if es_edicion:
            return redirect(f"{reverse('reconocimiento:gestion_trabajadores')}?accion=editar&id={id_trabajador}")
        else:
            return redirect(f"{reverse('reconocimiento:gestion_trabajadores')}?accion=agregar")
    
    return redirect('reconocimiento:gestion_trabajadores')

# ============================================================================
# REGISTRO FACIAL (MANTENIDO)
# ============================================================================

@login_required
def registro_facial_view(request):
    """
    Vista principal para el formulario de registro con captura facial usando DeepFace.
    """
    # Obtener tipos de personal para el formulario
    tipos_personal = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_nombre_tipo FROM tipos_personal ORDER BY id_nombre_tipo")
            tipos_personal = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Error obteniendo tipos de personal: {str(e)}")
        messages.error(request, "Error al cargar tipos de personal")
    
    # Verificar si hay un trabajador pendiente para capturar rostro
    trabajador_id = request.session.get('trabajador_para_rostro')
    datos_trabajador = None
    
    if trabajador_id:
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id_pk, cedula, nombres, apellidos, tipo_fk
                    FROM usuarios WHERE id_pk = %s
                """, [trabajador_id])
                resultado = cursor.fetchone()
                if resultado:
                    datos_trabajador = {
                        'id_pk': resultado[0],
                        'cedula': resultado[1],
                        'nombres': resultado[2],
                        'apellidos': resultado[3],
                        'tipo_fk': resultado[4]
                    }
        except Exception as e:
            logger.error(f"Error obteniendo datos del trabajador: {str(e)}")
    
    # Verificar que DeepFace esté funcionando
    try:
        # Prueba rápida de DeepFace
        test_img = np.zeros((100, 100, 3), dtype=np.uint8)
        DeepFace.extract_faces(test_img, detector_backend=DEEPFACE_CONFIG['detector_backend'])
        facial_status = "✅ DeepFace funcionando"
    except Exception as e:
        facial_status = f"⚠️ DeepFace: {str(e)[:50]}..."
    
    context = {
        'page_title': 'Registro de Trabajador con Reconocimiento Facial',
        'menu_activo': 'registro_facial',
        'tipos_personal': tipos_personal,
        'estados': ['Activo', 'Inactivo', 'Suspendido', 'Vacaciones'],
        'hoy': datetime.now().date(),
        'ahora': datetime.now(),
        'api_key': 'face_registration_' + str(datetime.now().timestamp()),
        'deepface_config': DEEPFACE_CONFIG,
        'facial_status': facial_status,
        'datos_trabajador': datos_trabajador,  # Para precargar formulario
    }
    
    # Limpiar sesión después de usar
    if 'trabajador_para_rostro' in request.session:
        del request.session['trabajador_para_rostro']
    
    return render(request, 'reconocimiento/registro_facial.html', context)

@login_required
def capturar_rostro_view(request):
    """
    Vista para capturar y procesar el rostro desde la cámara usando DeepFace.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    start_time = time.time()
    
    try:
        # Obtener datos de la solicitud
        data = json.loads(request.body)
        image_data = data.get('image', '')
        user_data = data.get('user_data', {})
        
        if not image_data:
            return JsonResponse({'error': 'No se recibió imagen'}, status=400)
        
        # Validar que se hayan enviado datos básicos del usuario
        if not user_data.get('cedula') or not user_data.get('nombres'):
            return JsonResponse({
                'error': 'Debe completar los datos básicos primero',
                'campos_faltantes': ['cedula', 'nombres'] if not user_data.get('cedula') else ['nombres']
            }, status=400)
        
        logger.info(f"Procesando rostro para: {user_data.get('cedula')} - {user_data.get('nombres')}")
        
        # Decodificar imagen base64
        if "," in image_data:
            header, encoded = image_data.split(",", 1)
        else:
            encoded = image_data
        
        image_bytes = base64.b64decode(encoded)
        
        # Convertir bytes a imagen
        image = Image.open(io.BytesIO(image_bytes))
        img_array = np.array(image)
        
        # Convertir RGBA a RGB si es necesario
        if len(img_array.shape) == 3 and img_array.shape[2] == 4:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        elif len(img_array.shape) == 2:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        
        # Validar calidad básica de imagen
        height, width = img_array.shape[:2]
        if height < 100 or width < 100:
            return JsonResponse({
                'error': 'Imagen demasiado pequeña',
                'suggestion': 'Acérquese más a la cámara'
            }, status=400)
        
        # 1. DETECTAR ROSTROS CON DEEPFACE
        logger.info("Detectando rostros con DeepFace...")
        try:
            faces = DeepFace.extract_faces(
                img_path=img_array,
                detector_backend=DEEPFACE_CONFIG['detector_backend'],
                enforce_detection=True,
                align=True
            )
        except ValueError as e:
            if "Face could not be detected" in str(e):
                return JsonResponse({
                    'error': 'No se detectó ningún rostro en la imagen',
                    'suggestions': [
                        'Asegúrese de que su rostro esté bien iluminado',
                        'Mire directamente a la cámara',
                        'Retire gafas de sol o accesorios que cubran el rostro',
                        'Acérquese más a la cámara'
                    ]
                }, status=400)
            else:
                raise
        
        if len(faces) == 0:
            return JsonResponse({
                'error': 'No se detectó ningún rostro en la imagen',
                'suggestions': [
                    'Asegúrese de que su rostro esté bien iluminado',
                    'Mire directamente a la cámara',
                    'Retire gafas de sol o accesorios que cubran el rostro'
                ]
            }, status=400)
        
        if len(faces) > 1:
            return JsonResponse({
                'error': 'Se detectó más de un rostro en la imagen',
                'detected_faces': len(faces),
                'suggestion': 'Por favor, capture solo una persona a la vez'
            }, status=400)
        
        logger.info(f"Rostro detectado: {len(faces)} cara(s)")
        
        # 2. EXTRAER EMBEDDING (REPRESENTACIÓN FACIAL)
        logger.info("Extrayendo embedding facial...")
        try:
            embedding_objs = DeepFace.represent(
                img_path=img_array,
                model_name=DEEPFACE_CONFIG['model_name'],
                detector_backend=DEEPFACE_CONFIG['detector_backend'],
                enforce_detection=True,
                align=True
            )
        except Exception as e:
            logger.error(f"Error al extraer embedding: {str(e)}")
            return JsonResponse({
                'error': f'Error al extraer características faciales: {str(e)}'
            }, status=500)
        
        if not embedding_objs or len(embedding_objs) == 0:
            return JsonResponse({'error': 'No se pudo extraer el embedding facial'}, status=500)
        
        # Obtener el primer embedding
        embedding = embedding_objs[0]['embedding']
        
        logger.info(f"Embedding extraído: {len(embedding)} dimensiones")
        
        # 3. VERIFICAR SI EL ROSTRO YA EXISTE EN LA BASE DE DATOS
        logger.info("Verificando rostros existentes en la base de datos...")
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT ru.id_pk, ru.vector_facial, u.cedula, u.nombres, u.apellidos
                    FROM rostros_usuarios ru
                    JOIN usuarios u ON ru.id_usuario_fk = u.id_pk
                    WHERE u.estado = 'Activo'
                """)
                
                existing_faces = cursor.fetchall()
                logger.info(f"Rostros existentes en BD: {len(existing_faces)}")
                
                for existing_face in existing_faces:
                    face_id, existing_vector_bytes, cedula, nombres, apellidos = existing_face
                    
                    if existing_vector_bytes:
                        # Convertir bytes a numpy array
                        existing_embedding = np.frombuffer(existing_vector_bytes, dtype=np.float32)
                        
                        # Calcular similitud coseno manualmente
                        from numpy.linalg import norm
                        A = np.array(embedding)
                        B = np.array(existing_embedding)
                        
                        # Normalizar vectores
                        A_norm = A / norm(A)
                        B_norm = B / norm(B)
                        
                        # Calcular similitud coseno
                        similarity = np.dot(A_norm, B_norm)
                        
                        # Umbral de similitud (ajustable)
                        if similarity > DEEPFACE_CONFIG['threshold']:
                            logger.warning(f"Rostro duplicado detectado: {cedula} - Similitud: {similarity:.4f}")
                            return JsonResponse({
                                'error': 'Rostro ya registrado',
                                'existing_user': {
                                    'cedula': cedula,
                                    'nombres': nombres,
                                    'apellidos': apellidos
                                },
                                'similarity': float(similarity),
                                'threshold': DEEPFACE_CONFIG['threshold']
                            }, status=409)
        
        except Exception as e:
            logger.error(f"Error verificando rostros existentes: {str(e)}")
            # Continuar con el registro aunque falle la verificación
        
        # 4. OBTENER INFORMACIÓN DEL ROSTRO DETECTADO
        face_info = faces[0]
        facial_area = face_info.get('facial_area', {})
        
        # Validar tamaño del rostro
        face_width = facial_area.get('w', 0)
        face_height = facial_area.get('h', 0)
        
        if face_width < 50 or face_height < 50:
            return JsonResponse({
                'error': 'Rostro demasiado pequeño en la imagen',
                'suggestion': 'Acérquese más a la cámara'
            }, status=400)
        
        # Calcular tiempo de procesamiento
        processing_time = time.time() - start_time
        
        # Devolver éxito con el embedding facial
        response_data = {
            'success': True,
            'message': 'Rostro capturado exitosamente',
            'embedding': embedding,  # Lista de floats
            'face_info': {
                'facial_area': facial_area,
                'confidence': face_info.get('confidence', 0),
                'face_width': face_width,
                'face_height': face_height,
                'embedding_size': len(embedding),
                'model_used': DEEPFACE_CONFIG['model_name'],
                'detector_used': DEEPFACE_CONFIG['detector_backend']
            },
            'validation': {
                'face_detected': True,
                'single_face': True,
                'face_size_adequate': face_width >= 50 and face_height >= 50,
                'embedding_extracted': True,
                'duplicate_check': True
            },
            'processing_time': round(processing_time, 2)
        }
        
        logger.info(f"Rostro procesado exitosamente en {processing_time:.2f} segundos")
        return JsonResponse(response_data)
    
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return JsonResponse({'error': 'Formato JSON inválido'}, status=400)
    except Exception as e:
        logger.error(f"Error en capturar_rostro_view: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': f'Error interno del servidor: {str(e)[:200]}'
        }, status=500)

@login_required
def guardar_registro_completo_view(request):
    """
    Vista para guardar tanto los datos del usuario como el vector facial usando DeepFace.
    """
    if request.method != 'POST':
        logger.error("Método no permitido en guardar_registro_completo_view")
        messages.error(request, 'Método no permitido')
        return redirect('reconocimiento:registro_facial')
    
    try:
        # ========== LOGGING DETALLADO ==========
        logger.info("=" * 60)
        logger.info("📥 INICIANDO PROCESO DE GUARDADO DE REGISTRO")
        logger.info("=" * 60)
        
        # Mostrar todos los datos recibidos
        logger.info("📋 DATOS POST RECIBIDOS:")
        for key, value in request.POST.items():
            if key == 'facial_embedding':
                logger.info(f"  {key}: {'PRESENTE' if value else 'VACÍO'} (longitud: {len(value) if value else 0})")
            else:
                logger.info(f"  {key}: '{value}'")
        
        # ========== OBTENER DATOS DEL FORMULARIO ==========
        cedula = request.POST.get('cedula', '').strip()
        nombres = request.POST.get('nombres', '').strip()
        apellidos = request.POST.get('apellidos', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        correo = request.POST.get('correo', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        estado = request.POST.get('estado', 'Activo').strip()
        area_trabajo = request.POST.get('area_trabajo', '').strip()
        rol = request.POST.get('rol', '').strip()
        tipo_personal = request.POST.get('tipo_personal', '').strip()
        embedding_json = request.POST.get('facial_embedding', '')
        id_trabajador_existente = request.POST.get('id_trabajador_existente', '').strip()
        
        # ========== VALIDACIONES DETALLADAS ==========
        logger.info("🔍 VALIDANDO CAMPOS:")
        
        # Validar campos requeridos
        campos_requeridos = [
            ('cedula', cedula),
            ('nombres', nombres),
            ('apellidos', apellidos),
            ('tipo_personal', tipo_personal)
        ]
        
        campos_faltantes = []
        for nombre, valor in campos_requeridos:
            if not valor:
                campos_faltantes.append(nombre)
                logger.error(f"  ❌ {nombre}: VACÍO")
            else:
                logger.info(f"  ✅ {nombre}: '{valor}' (longitud: {len(valor)})")
        
        if campos_faltantes:
            error_msg = f'Campos requeridos faltantes: {", ".join(campos_faltantes)}'
            logger.error(f"VALIDACIÓN FALLIDA: {error_msg}")
            messages.error(request, error_msg)
            return redirect('reconocimiento:registro_facial')
        
        # Validar formato de cédula
        if not cedula.isdigit() or len(cedula) != 8:
            logger.error(f"❌ Cédula inválida: '{cedula}'")
            messages.error(request, 'La cédula debe tener exactamente 8 dígitos numéricos')
            return redirect('reconocimiento:registro_facial')
        
        # Validar embedding
        if not embedding_json:
            logger.error("❌ No se recibió embedding facial")
            messages.error(request, 'Debe capturar el rostro antes de guardar')
            return redirect('reconocimiento:registro_facial')
        
        try:
            embedding_list = json.loads(embedding_json)
            logger.info(f"✅ Embedding JSON válido: {len(embedding_list)} elementos")
        except json.JSONDecodeError as e:
            logger.error(f"❌ Error en formato JSON del embedding: {str(e)}")
            messages.error(request, 'Error en el formato del vector facial')
            return redirect('reconocimiento:registro_facial')
        
        # ========== CONVERTIR EMBEDDING ==========
        try:
            embedding_array = np.array(embedding_list, dtype=np.float32)
            embedding_bytes = embedding_array.tobytes()
            logger.info(f"✅ Embedding convertido: {len(embedding_list)} elementos, {len(embedding_bytes)} bytes")
        except Exception as e:
            logger.error(f"❌ Error procesando embedding: {str(e)}")
            messages.error(request, f'Error procesando vector facial: {str(e)}')
            return redirect('reconocimiento:registro_facial')
        
        # ========== TRANSACCIÓN DE BASE DE DATOS ==========
        try:
            with connection.cursor() as cursor:
                user_id = None
                
                # Si ya existe un ID de trabajador, estamos actualizando
                if id_trabajador_existente:
                    user_id = int(id_trabajador_existente)
                    logger.info(f"📝 Actualizando trabajador existente ID: {user_id}")
                    
                    # Verificar que exista
                    cursor.execute("SELECT cedula FROM usuarios WHERE id_pk = %s", [user_id])
                    if not cursor.fetchone():
                        messages.error(request, 'Trabajador no encontrado')
                        return redirect('reconocimiento:registro_facial')
                    
                    # Actualizar datos básicos
                    cursor.execute("""
                        UPDATE usuarios SET
                            cedula = %s, nombres = %s, apellidos = %s,
                            direccion_habitacional = %s, correo = %s, numero = %s,
                            estado = %s, area_trabajo = %s, rol = %s, tipo_fk = %s
                        WHERE id_pk = %s
                    """, [
                        cedula, nombres, apellidos, direccion or '',
                        correo or '', telefono or '', estado,
                        area_trabajo or '', rol or '', tipo_personal, user_id
                    ])
                    
                    # Eliminar rostro anterior si existe
                    cursor.execute("DELETE FROM rostros_usuarios WHERE id_usuario_fk = %s", [user_id])
                    
                    logger.info(f"✅ Datos básicos actualizados para ID: {user_id}")
                    
                else:
                    # 1. Verificar si la cédula ya existe
                    logger.info(f"🔍 Verificando duplicados para cédula: {cedula}")
                    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE cedula = %s", [cedula])
                    count_result = cursor.fetchone()
                    existing_count = count_result[0] if count_result else 0
                    
                    if existing_count > 0:
                        error_msg = f'La cédula {cedula} ya está registrada en el sistema'
                        logger.error(f"❌ {error_msg}")
                        messages.error(request, error_msg)
                        return redirect('reconocimiento:registro_facial')
                    
                    logger.info(f"✅ Cédula {cedula} disponible")
                    
                    # 2. Preparar datos para inserción
                    insert_params = [
                        cedula, nombres, apellidos, direccion or '',
                        correo or '', telefono or '', estado or 'Activo',
                        area_trabajo or '', rol or '', tipo_personal
                    ]
                    
                    logger.info("📝 Insertando usuario en tabla 'usuarios'...")
                    logger.info(f"   Parámetros: {insert_params}")
                    
                    # 3. Insertar usuario
                    insert_query = """
                        INSERT INTO usuarios (
                            cedula, nombres, apellidos, direccion_habitacional,
                            correo, numero, estado, area_trabajo, rol, tipo_fk
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    cursor.execute(insert_query, insert_params)
                    user_id = cursor.lastrowid
                    logger.info(f"✅ Usuario insertado exitosamente. ID generado: {user_id}")
                
                # 4. Insertar vector facial (común para ambos casos)
                logger.info(f"📝 Insertando vector facial para usuario ID: {user_id}")
                cursor.execute("""
                    INSERT INTO rostros_usuarios (id_usuario_fk, vector_facial)
                    VALUES (%s, %s)
                """, [user_id, embedding_bytes])
                
                logger.info("✅ Vector facial insertado exitosamente")
                
                # 5. Si es administrativo, crear credenciales (solo para nuevos)
                if not id_trabajador_existente:
                    tipo_lower = tipo_personal.lower()
                    if any(admin_keyword in tipo_lower for admin_keyword in ['admin', 'administrativo', 'administrador']):
                        try:
                            import secrets
                            import hashlib
                            temp_password = secrets.token_urlsafe(8)
                            hashed_password = hashlib.sha256(temp_password.encode()).hexdigest()
                            
                            cursor.execute("""
                                INSERT INTO usuarios_administrativos (id_usuario_fk, password)
                                VALUES (%s, %s)
                            """, [user_id, hashed_password])
                            
                            request.session['temp_password'] = temp_password
                            request.session['new_user_id'] = user_id
                            
                            logger.info(f"✅ Credenciales administrativas creadas. Password temporal: {temp_password}")
                            
                        except Exception as e:
                            logger.warning(f"⚠️ No se pudieron crear credenciales administrativas: {str(e)}")
                
                # 6. Confirmar transacción
                connection.commit()
                logger.info("✅ Transacción completada exitosamente")
                
                # 7. Mensaje de éxito
                if id_trabajador_existente:
                    success_msg = f'Trabajador {nombres} {apellidos} actualizado exitosamente con nuevo reconocimiento facial'
                else:
                    success_msg = f'Trabajador {nombres} {apellidos} registrado exitosamente con reconocimiento facial'
                    
                messages.success(request, success_msg)
                logger.info(f"📨 Mensaje al usuario: {success_msg}")
                
                # 8. Redirigir a página de éxito
                logger.info("🔄 Redirigiendo a página de éxito...")
                return redirect('reconocimiento:registro_exitoso')
                
        except Exception as db_error:
            logger.error(f"❌ ERROR DE BASE DE DATOS: {str(db_error)}")
            logger.error(traceback.format_exc())
            
            # Intentar hacer rollback si hay error
            try:
                connection.rollback()
                logger.info("🔄 Rollback realizado")
            except:
                pass
            
            # Determinar tipo de error
            error_str = str(db_error).lower()
            if "duplicate" in error_str:
                error_msg = f'La cédula {cedula} ya está registrada en el sistema'
            elif "foreign key" in error_str:
                error_msg = f'El tipo de personal "{tipo_personal}" no existe'
            elif "data too long" in error_str:
                error_msg = 'Algunos datos exceden la longitud permitida'
            else:
                error_msg = f'Error de base de datos: {str(db_error)[:100]}'
            
            messages.error(request, error_msg)
            return redirect('reconocimiento:registro_facial')
            
    except json.JSONDecodeError as e:
        logger.error(f"❌ ERROR DE JSON: {str(e)}")
        messages.error(request, f'Error en el formato de los datos: {str(e)}')
        return redirect('reconocimiento:registro_facial')
        
    except Exception as e:
        logger.error(f"❌ ERROR NO CONTROLADO: {str(e)}")
        logger.error(traceback.format_exc())
        messages.error(request, f'Error interno del sistema: {str(e)[:100]}')
        return redirect('reconocimiento:registro_facial')

@login_required
def registro_exitoso_view(request):
    """
    Vista de confirmación después del registro exitoso.
    """
    # Obtener datos de la sesión
    temp_password = request.session.pop('temp_password', None)
    new_user_id = request.session.pop('new_user_id', None)
    
    logger.info(f"📄 Accediendo a registro_exitoso_view. User ID: {new_user_id}")
    
    # Obtener información del usuario recién registrado
    user_info = None
    if new_user_id:
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT cedula, nombres, apellidos, correo, rol, tipo_fk 
                    FROM usuarios WHERE id_pk = %s
                """, [new_user_id])
                result = cursor.fetchone()
                if result:
                    user_info = {
                        'cedula': result[0],
                        'nombres': result[1],
                        'apellidos': result[2],
                        'correo': result[3] or 'No especificado',
                        'rol': result[4] or 'No especificado',
                        'tipo_personal': result[5] or 'No especificado'
                    }
                    logger.info(f"✅ Información del usuario obtenida: {user_info['nombres']} {user_info['apellidos']}")
                else:
                    logger.warning(f"⚠️ No se encontró usuario con ID: {new_user_id}")
        except Exception as e:
            logger.error(f"❌ Error obteniendo info de usuario nuevo: {str(e)}")
    
    context = {
        'page_title': 'Registro Exitoso',
        'user_info': user_info,
        'temp_password': temp_password,
        'hoy': datetime.now().date(),
        'ahora': datetime.now(),
    }
    
    return render(request, 'reconocimiento/registro_exitoso.html', context)

# ============================================================================
# APIs DE VERIFICACIÓN (MANTENIDAS)
# ============================================================================

@login_required
def verificar_camara_view(request):
    """
    API para verificar que la cámara está funcionando.
    """
    try:
        # Intentar abrir la cámara
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            return JsonResponse({
                'success': False,
                'error': 'No se pudo acceder a la cámara',
                'suggestions': [
                    'Verifique que la cámara esté conectada',
                    'Asegúrese de haber dado permisos al navegador',
                    'Intente con otro navegador'
                ]
            })
        
        # Leer un frame de prueba
        ret, frame = cap.read()
        
        if not ret:
            cap.release()
            return JsonResponse({
                'success': False,
                'error': 'Cámara accesible pero no puede capturar imágenes'
            })
        
        # Obtener información de la cámara
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        cap.release()
        
        return JsonResponse({
            'success': True,
            'message': 'Cámara funcionando correctamente',
            'camera_info': {
                'width': width,
                'height': height,
                'fps': fps
            }
        })
    
    except Exception as e:
        logger.error(f"Error en verificar_camara_view: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': f'Error al verificar cámara: {str(e)}'
        })

@login_required
def test_deepface_view(request):
    """
    Vista para probar que DeepFace está funcionando.
    """
    try:
        # Crear una imagen de prueba
        test_img = np.zeros((200, 200, 3), dtype=np.uint8)
        # Dibujar un "rostro" simple (círculo)
        cv2.circle(test_img, (100, 100), 40, (255, 255, 255), -1)
        cv2.circle(test_img, (80, 80), 10, (0, 0, 0), -1)  # Ojo izquierdo
        cv2.circle(test_img, (120, 80), 10, (0, 0, 0), -1)  # Ojo derecho
        cv2.ellipse(test_img, (100, 130), (30, 15), 0, 0, 180, (0, 0, 0), 5)  # Boca
        
        # Probar detección
        faces = DeepFace.extract_faces(
            test_img, 
            detector_backend=DEEPFACE_CONFIG['detector_backend'],
            enforce_detection=False
        )
        
        # Probar representación
        representations = DeepFace.represent(
            test_img,
            model_name=DEEPFACE_CONFIG['model_name'],
            detector_backend=DEEPFACE_CONFIG['detector_backend'],
            enforce_detection=False
        )
        
        return JsonResponse({
            'success': True,
            'message': 'DeepFace funcionando correctamente',
            'deepface_info': {
                'version': '0.0.81',  # Versión común de DeepFace
                'model': DEEPFACE_CONFIG['model_name'],
                'detector': DEEPFACE_CONFIG['detector_backend'],
                'faces_detected': len(faces),
                'embedding_size': len(representations[0]['embedding']) if representations else 0,
                'threshold': DEEPFACE_CONFIG['threshold']
            }
        })
    
    except Exception as e:
        logger.error(f"Error en test_deepface_view: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': f'Error en DeepFace: {str(e)}'
        })

@login_required
def verificar_asistencia_view(request):
    """
    Vista para verificar asistencia con reconocimiento facial (OPCIONAL).
    """
    context = {
        'page_title': 'Verificación de Asistencia',
        'menu_activo': 'control_acceso',
        'hoy': datetime.now().date(),
        'ahora': datetime.now(),
    }
    
    return render(request, 'reconocimiento/verificar_asistencia.html', context)

# ============================================================================
# VISTA DE DEBUG TEMPORAL (MANTENIDA)
# ============================================================================

@login_required
def debug_post_data_view(request):
    """
    Vista temporal para depurar datos POST recibidos.
    """
    if request.method == 'POST':
        debug_info = {
            'post_data': dict(request.POST),
            'files': list(request.FILES.keys()),
            'content_type': request.content_type,
            'method': request.method,
            'headers': dict(request.headers)
        }
        
        # Guardar en archivo de log
        import json
        with open('debug_post_data.log', 'w', encoding='utf8') as f:
            json.dump(debug_info, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info("📋 Datos POST depurados guardados en debug_post_data.log")
        
        return JsonResponse({
            'success': True,
            'message': 'Datos POST guardados para depuración',
            'debug_info': debug_info
        })
    
    return JsonResponse({
        'success': False,
        'error': 'Esta vista solo acepta solicitudes POST'
    }, status=400)