from django.urls import path
from . import views
from . import api_views

app_name = 'citas_ecografia'

urlpatterns = [
    path('', views.citas_ecografia_list, name='list'),
    # Esto le aparece al ecógrafo de las citas que tiene que atender (mis-citas)
    path('mis-citas/', views.mis_citas_ecografia, name='mis_citas'),
    path('pacientes-atendidos/', views.pacientes_atendidos_ecografia, name='pacientes_atendidos'),
    path('mis-citas/<int:cita_id>/detalle/', views.ver_detalle_cita_ecografia, name='detalle_cita'),
    path('mis-citas/<int:cita_id>/atender/', views.atender_cita_ecografia, name='atender_cita'),
    path('mis-citas/<int:cita_id>/guardar-resultado/', views.guardar_resultado_cita, name='guardar_resultado'),
    path('agendar/', views.agendar_cita_ecografia, name='agendar'),
    path('buscar-paciente/', views.buscar_paciente_ecografia, name='buscar_paciente'),
    path('obtener-horarios/', views.obtener_horarios_medico, name='obtener_horarios'),
    path('obtener-horarios-ecografo/', views.obtener_horarios_ecografo, name='obtener_horarios_ecografo'),
    path('verificar-dias-ocupados/<int:ecografo_id>/', views.verificar_dias_ocupados_ecografo, name='verificar_dias_ocupados'),
    path('api/ecografo/<int:ecografo_id>/', api_views.api_ecografo_info, name='api_ecografo'),
    path('crear/', views.crear_cita_ecografia, name='crear'),
    path('<int:cita_id>/editar/', views.editar_cita_ecografia, name='editar'),
    path('<int:cita_id>/cancelar/', views.cancelar_cita_ecografia, name='cancelar'),
    path('<int:cita_id>/pdf/', views.generar_pdf_cita, name='generar_pdf'),
]
