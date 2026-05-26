from django.urls import path
from . import views

app_name = 'asistencia'

urlpatterns = [
    path('', views.lista_asistencia_view, name='lista'),
    path('<int:registro_id>/', views.detalle_asistencia_view, name='detalle'),
]