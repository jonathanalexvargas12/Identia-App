from django.urls import path
from . import views

app_name = 'notificaciones'

urlpatterns = [
    # Vista principal
    path('', views.bitacora_incidentes_view, name='bitacora'),
    path('bitacora/', views.bitacora_incidentes_view, name='bitacora_incidentes'),
    path('bitacora/pdf/', views.bitacora_pdf, name='bitacora_pdf'),
    
    # APIs para notificaciones - SOLO LEÍDAS
    path('api/notificaciones/', views.api_notificaciones, name='api_notificaciones'),
    path('api/contador-no-leidas/', views.api_contador_no_leidas, name='api_contador_no_leidas'),
    path('api/marcar-leida/', views.api_marcar_leida, name='api_marcar_leida'),
    path('api/marcar-todas-leidas/', views.api_marcar_todas_leidas, name='api_marcar_todas_leidas'),
]