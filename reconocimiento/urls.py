# reconocimiento/urls.py
from django.urls import path
from . import views

app_name = 'reconocimiento'

urlpatterns = [
    # CRUD de trabajadores
    path('gestion-trabajadores/', views.gestion_trabajadores_view, name='gestion_trabajadores'),
    path('guardar-trabajador/', views.guardar_trabajador_view, name='guardar_trabajador'),
    
    # Registro facial
    path('registro-facial/', views.registro_facial_view, name='registro_facial'),
    path('capturar-rostro/', views.capturar_rostro_view, name='capturar_rostro'),
    path('guardar-registro-completo/', views.guardar_registro_completo_view, name='guardar_registro_completo'),
    path('registro-exitoso/', views.registro_exitoso_view, name='registro_exitoso'),
    
    # APIs de verificación
    path('verificar-camara/', views.verificar_camara_view, name='verificar_camara'),
    path('test-deepface/', views.test_deepface_view, name='test_deepface'),
    path('verificar-asistencia/', views.verificar_asistencia_view, name='verificar_asistencia'),
    
    # Debug
    path('debug-post-data/', views.debug_post_data_view, name='debug_post_data'),
]