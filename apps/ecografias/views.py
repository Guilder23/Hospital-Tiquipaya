from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, JsonResponse
from django import forms
from apps.accounts.models import Perfil, Ecografo
from apps.especialidades.models import Especialidad
from apps.permisos.utils import es_admin_o_staff
from .models import Ecografia


def _es_admin(user):
    return es_admin_o_staff(user)


class EcografiaBaseForm(forms.ModelForm):
    class Meta:
        model = Ecografia
        fields = ['nombre', 'ecografo', 'especialidad', 'descripcion']


class EcografiaCreateForm(EcografiaBaseForm):
    pass


class EcografiaUpdateForm(forms.ModelForm):
    class Meta:
        model = Ecografia
        fields = ['nombre', 'ecografo', 'especialidad', 'descripcion', 'estado']


class EcografiaListView(LoginRequiredMixin, ListView):
    model = Ecografia
    template_name = 'ecografias/ecografias.html'
    context_object_name = 'ecografias'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['permiso_actual'] = getattr(self.request, 'permiso_actual', None)
        ctx['ecografos'] = Ecografo.objects.all()
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
        permiso = getattr(self.request, 'permiso_actual', None)
        return permiso and permiso.puede_editar() if permiso else False
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = 'INACTIVA'
        self.object.save(update_fields=['estado'])
        return HttpResponseRedirect(self.get_success_url())
