from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Turnos
from django.urls import reverse_lazy

# 1. Vista para listar todos los turnos
class TurnoListView(ListView):
    model = Turnos
    template_name = 'turnos/turno_list.html'
    context_object_name = 'lista_turnos'

# 2. Vista para ver los detalles de un turno específico
class TurnoDetailView(DetailView):
    model = Turnos
    template_name = 'turnos/turno_detail.html'
    context_object_name = 'turno'

# 3. Vista para crear un nuevo turno
class TurnoCreateView(CreateView):
    model = Turnos
    fields = ['nombre', 'hora_ini', 'hora_fin']
    success_url = reverse_lazy('turnos:lista')
    template_name = 'turnos/turno_form.html'