from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
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

class PacienteBaseForm(forms.ModelForm):
    def clean_tiene_seguro(self):
        val = self.data.get('tiene_seguro', self.cleaned_data.get('tiene_seguro'))
        if isinstance(val, str):
            v = val.strip().lower()
            return v in ('true','1','on','yes','si')
        return bool(val)

class PacienteCreateForm(PacienteBaseForm):
    class Meta:
        model = Paciente
        fields = [
            'nombres','apellido_paterno','apellido_materno',
            'ci','ci_complemento','expedido',
            'fecha_nacimiento','genero',
            'telefono_fijo','celular','email',
            'zona','calle','numero_domicilio','direccion',
            'nacionalidad',
            'tiene_seguro','numero_seguro',
            'emergencia_nombre','emergencia_telefono','emergencia_relacion',
        ]

class PacienteUpdateForm(PacienteBaseForm):
    class Meta:
        model = Paciente
        fields = [
            'nombres','apellido_paterno','apellido_materno',
            'ci','ci_complemento','expedido',
            'fecha_nacimiento','genero',
            'telefono_fijo','celular','email',
            'zona','calle','numero_domicilio','direccion',
            'nacionalidad',
            'tiene_seguro','numero_seguro',
            'emergencia_nombre','emergencia_telefono','emergencia_relacion',
            'activo'
        ]

class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = 'pacientes/pacientes.html'
    context_object_name = 'pacientes'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['puede_admin'] = _es_admin(self.request.user)
        return ctx

class PacienteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = PacienteCreateForm
    template_name = 'pacientes/pacientes.html'
    success_url = reverse_lazy('paciente_list')
    def test_func(self):
        return _es_admin(self.request.user)
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.activo = True
        obj.save()
        self.object = obj
        return HttpResponseRedirect(self.get_success_url())
    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

class PacienteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Paciente
    form_class = PacienteUpdateForm
    template_name = 'pacientes/pacientes.html'
    success_url = reverse_lazy('paciente_list')
    def test_func(self):
        return _es_admin(self.request.user)
    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

class PacienteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Paciente
    template_name = 'pacientes/confirm_delete.html'
    success_url = reverse_lazy('paciente_list')
    def test_func(self):
        return _es_admin(self.request.user)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save(update_fields=['activo'])
        return HttpResponseRedirect(self.get_success_url())