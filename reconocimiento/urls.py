# reconocimiento/urls.py
from django.urls import path
from . import views

app_name = 'reconocimiento'

urlpatterns = [
    # ============================================================================
    # CRUD DE TRABAJADORES
    # ============================================================================
    path('gestion-trabajadores/', views.gestion_trabajadores_view, name='gestion_trabajadores'),
    path('guardar-trabajador/', views.guardar_trabajador_view, name='guardar_trabajador'),
    
    # ============================================================================
    # REGISTRO FACIAL
    # ============================================================================
    path('registro-facial/', views.registro_facial_view, name='registro_facial'),
    path('capturar-rostro/', views.capturar_rostro_view, name='capturar_rostro'),
    path('guardar-registro-completo/', views.guardar_registro_completo_view, name='guardar_registro_completo'),
    path('registro-exitoso/', views.registro_exitoso_view, name='registro_exitoso'),
    
    # ============================================================================
    # CONTROL DE ACCESO - NUEVAS RUTAS
    # ============================================================================
    # Vista principal de control de acceso (interfaz con cámara)
    path('control-acceso/', views.control_acceso_view, name='control_acceso'),
    
    # API para verificar rostro en tiempo real (usada por la cámara)
    path('api/verificar-rostro/', views.verificar_rostro_acceso_view, name='verificar_rostro'),
    
    # API para verificar estado de un usuario específico (útil para debugging)
    path('api/verificar-estado/<int:usuario_id>/', views.verificar_estado_usuario_view, name='verificar_estado'),
    
    # API para comparar dos usuarios y detectar posibles duplicados
    path('api/comparar-usuarios/', views.comparar_usuarios_view, name='comparar_usuarios'),
    
    # API para ajustar el umbral de reconocimiento (solo administradores)
    path('api/ajustar-umbral/', views.ajustar_umbral_view, name='ajustar_umbral'),
    
    # ============================================================================
    # APIs DE VERIFICACIÓN (EXISTENTES)
    # ============================================================================
    path('verificar-camara/', views.verificar_camara_view, name='verificar_camara'),
    path('test-deepface/', views.test_deepface_view, name='test_deepface'),
    path('verificar-asistencia/', views.verificar_asistencia_view, name='verificar_asistencia'),
    
    # ============================================================================
    # DEBUG
    # ============================================================================
    path('debug-post-data/', views.debug_post_data_view, name='debug_post_data'),
]