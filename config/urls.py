"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    
    # Redirección raíz
    path('', redirect_to_login),
]

# Configurar handlers de error personalizados
handler404 = 'usuarios.views.handler404'
handler500 = 'usuarios.views.handler500'
handler403 = 'usuarios.views.handler403'
handler400 = 'usuarios.views.handler400'
