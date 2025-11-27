from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms
from apps.accounts.models import Perfil, TipoUsuario
from apps.citas.models import Cita
from .models import Paciente
from datetime import datetime

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


@login_required
def mis_citas_atendidas(request):
    """Vista que muestra las citas atendidas del paciente autenticado"""
    # Intenta obtener el paciente del usuario actual
    # Primero intenta por Perfil (si el usuario es también un perfil)
    try:
        perfil = request.user.perfil
        paciente = Paciente.objects.get(ci=perfil.ci)
    except (AttributeError, Perfil.DoesNotExist, Paciente.DoesNotExist):
        # Si no encuentra por CI, intenta por nombre
        try:
            paciente = Paciente.objects.get(nombres=request.user.first_name)
        except Paciente.DoesNotExist:
            # Si tampoco encuentra, redirige al home
            return redirect('home')
    
    # Obtener todas las citas atendidas del paciente
    citas_atendidas = Cita.objects.filter(
        paciente=paciente,
        estado_atencion='ATENDIDO'
    ).select_related('medico', 'especialidad', 'medico__user__perfil').order_by('-tiempo_fin_atencion')
    
    context = {
        'paciente': paciente,
        'citas_atendidas': citas_atendidas,
        'fecha': datetime.now().date(),
    }
    
    return render(request, 'pacientes/mis_citas_atendidas.html', context)