from django.urls import path
from . import views

app_name = 'citas_ecografia'

urlpatterns = [
    path('', views.citas_ecografia_list, name='list'),
    path('agendar/', views.agendar_cita_ecografia, name='agendar'),
    path('buscar-paciente/', views.buscar_paciente_ecografia, name='buscar_paciente'),
    path('obtener-horarios/', views.obtener_horarios_medico, name='obtener_horarios'),
    path('crear/', views.crear_cita_ecografia, name='crear'),
    path('<int:cita_id>/editar/', views.editar_cita_ecografia, name='editar'),
    path('<int:cita_id>/cancelar/', views.cancelar_cita_ecografia, name='cancelar'),
]
