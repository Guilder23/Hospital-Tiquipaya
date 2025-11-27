from django.urls import path
from .views import PacienteListView, PacienteCreateView, PacienteUpdateView, PacienteDeleteView, mis_citas_atendidas

urlpatterns = [
    path('', PacienteListView.as_view(), name='paciente_list'),
    path('nuevo/', PacienteCreateView.as_view(), name='paciente_create'),
    path('<int:pk>/editar/', PacienteUpdateView.as_view(), name='paciente_update'),
    path('<int:pk>/eliminar/', PacienteDeleteView.as_view(), name='paciente_delete'),
    path('mis-citas-atendidas/', mis_citas_atendidas, name='mis_citas_atendidas'),
]