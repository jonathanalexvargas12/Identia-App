# usuarios/urls.py (VERSIÓN ACTUALIZADA)
from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Home principal con menú lateral
    path('', views.home_principal_view, name='home_principal'),
    
    # Dashboard y perfil
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('perfil/', views.perfil_view, name='perfil'),
    
    # Módulos del menú lateral (actualizados)
    path('control-acceso/', views.control_acceso_view, name='control_acceso'),
    path('buscar-trabajadores/', views.buscar_trabajadores_view, name='buscar_trabajadores'),
    
    # API para hora actual
    path('get-current-time/', views.get_current_time_view, name='get_current_time'),
    
    # CRUD para Tipos de Personal
    path('gestion-tipos-personal/', views.gestion_tipos_personal_view, name='gestion_tipos_personal'),
    path('gestion-horarios/', views.gestion_horarios_view, name='gestion_horarios'),

    
    # Otros módulos
    path('seguridad/', views.seguridad_view, name='seguridad'),
    path('reportes/', views.reportes_view, name='reportes'),
    path('modulos-gestion/', views.modulos_gestion_view, name='modulos_gestion'),
    
    # Páginas públicas
    path('home/', views.home_view, name='home'),
    path('acerca/', views.acerca_view, name='acerca'),
    path('ayuda/', views.ayuda_view, name='ayuda'),
    
    # Vistas de desarrollo/debug (solo en modo DEBUG)
    path('debug/session/', views.debug_session_view, name='debug_session'),
    path('debug/test-auth/', views.test_auth_view, name='test_auth'),
]