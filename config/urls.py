# config/urls.py
"""
URLs principales del proyecto.
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from usuarios import views as views

def redirect_to_login(request):
    """Redirige la raíz a la página de inicio"""
    return redirect('usuarios:login')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Aplicación de usuarios
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),

    # Incluir URLs de reconocimiento 
    path('reconocimiento/', include('reconocimiento.urls')),

    # Incluir URLs de asistencia
    path('asistencia/', include('asistencia.urls')),

     # Incluir URLs de notificaciones
    path('notificaciones/', include('notificaciones.urls')),
    
    # Incluir URLs de reportes
    path('reportes/', include('reportes.urls', namespace='reportes')),
    
    # Redirección raíz
    path('', redirect_to_login),
]

# Configurar handlers de error personalizados
handler404 = 'usuarios.views.handler404'
handler500 = 'usuarios.views.handler500'
handler403 = 'usuarios.views.handler403'
handler400 = 'usuarios.views.handler400'