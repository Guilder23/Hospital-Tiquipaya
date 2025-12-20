from django.urls import path
from . import views

app_name = 'permisos'

urlpatterns = [
    # Listado de tipos de usuario para gestión de permisos
    path('tipos/', views.listar_tipos, name='listar_tipos'),
    # Asignación de permisos por tipo de usuario
    path('asignar/<int:tipo_id>/', views.asignar_permisos, name='asignar_permisos'),
]
