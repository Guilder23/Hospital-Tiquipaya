from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_especialidades, name='lista_especialidades'),
    path('crear/', views.crear_especialidad, name='crear_especialidad'),
    path('editar/<int:id>/', views.editar_especialidad, name='editar_especialidad'),
    path('activar/<int:id>/', views.activar_especialidad, name='activar_especialidad'),
    path('desactivar/<int:id>/', views.desactivar_especialidad, name='desactivar_especialidad'),
]
