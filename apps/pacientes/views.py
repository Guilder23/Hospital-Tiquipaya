from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django import forms
from apps.accounts.models import Perfil, TipoUsuario
from .models import Paciente

def _es_admin(user):
    if user.is_superuser or user.is_staff:
        return True
    try:
        perfil = user.perfil
    except Perfil.DoesNotExist:
        return False
    if perfil.tipo is None:
        return False
    return perfil.tipo.nombre.lower() == 'administrador'

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['ci','expedido','nombres','apellidos','fecha_nacimiento','genero','nacionalidad','telefono','email','direccion','tiene_seguro','numero_seguro','emergencia_nombre','emergencia_telefono','emergencia_relacion']

class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = 'pacientes/pacientes.html'
    context_object_name = 'pacientes'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['puede_admin'] = _es_admin(self.request.user)
        return ctx

class PacienteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = PacienteForm
    template_name = 'pacientes/form.html'
    success_url = reverse_lazy('paciente_list')
    def test_func(self):
        return _es_admin(self.request.user)

class PacienteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/form.html'
    success_url = reverse_lazy('paciente_list')
    def test_func(self):
        return _es_admin(self.request.user)

class PacienteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Paciente
    template_name = 'pacientes/confirm_delete.html'
    success_url = reverse_lazy('paciente_list')
    def test_func(self):
        return _es_admin(self.request.user)