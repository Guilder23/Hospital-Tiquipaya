from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, JsonResponse
from django import forms
from apps.accounts.models import Perfil, Medico
from apps.especialidades.models import Especialidad
from .models import Ecografia


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


class EcografiaBaseForm(forms.ModelForm):
    class Meta:
        model = Ecografia
        fields = ['nombre', 'medico', 'especialidad', 'descripcion']


class EcografiaCreateForm(EcografiaBaseForm):
    pass


class EcografiaUpdateForm(forms.ModelForm):
    class Meta:
        model = Ecografia
        fields = ['nombre', 'medico', 'especialidad', 'descripcion', 'estado']


class EcografiaListView(LoginRequiredMixin, ListView):
    model = Ecografia
    template_name = 'ecografias/ecografias.html'
    context_object_name = 'ecografias'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['puede_admin'] = _es_admin(self.request.user)
        ctx['medicos'] = Medico.objects.all()
        ctx['especialidades'] = Especialidad.objects.all()
        return ctx


class EcografiaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = EcografiaCreateForm
    template_name = 'ecografias/ecografias.html'
    success_url = reverse_lazy('ecografia_list')
    
    def test_func(self):
        return _es_admin(self.request.user)
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.generar_codigo()
        obj.estado = 'ACTIVA'
        obj.save()
        self.object = obj
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)


class EcografiaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ecografia
    form_class = EcografiaUpdateForm
    template_name = 'ecografias/ecografias.html'
    success_url = reverse_lazy('ecografia_list')
    
    def test_func(self):
        return _es_admin(self.request.user)
    
    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)


class EcografiaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ecografia
    template_name = 'ecografias/confirm_delete.html'
    success_url = reverse_lazy('ecografia_list')
    
    def test_func(self):
        return _es_admin(self.request.user)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 'INACTIVA'
        self.object.save(update_fields=['estado'])
        return HttpResponseRedirect(self.get_success_url())
