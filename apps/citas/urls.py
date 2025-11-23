from django.urls import path
from . import views

app_name = 'citas'

urlpatterns = [
    path('validar/', views.validar_paciente, name='validar'),
    path('agendar/', views.agendar_inicio, name='agendar'),
    path('agenda/<int:medico_id>/', views.agenda_medico, name='agenda_medico'),
    path('confirmar/', views.confirmar_cita, name='confirmar'),
    path('orden/<int:cita_id>/', views.orden_html, name='orden'),
    path('mis/', views.mis_citas, name='mis'),
    path('<int:cita_id>/editar/', views.editar_cita, name='editar'),
    path('<int:cita_id>/cancelar/', views.cancelar_cita, name='cancelar'),
    path('logout/', views.logout_paciente, name='logout'),
]
