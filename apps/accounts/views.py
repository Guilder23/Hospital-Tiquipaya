from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth import get_user_model
from django import forms
from .models import TipoUsuario, PerfilUsuario
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class TipoUsuarioListView(LoginRequiredMixin, ListView):
    model = TipoUsuario
    template_name = 'accounts/tipos/list.html'

class TipoUsuarioCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = TipoUsuario
    fields = ['nombre','descripcion']
    template_name = 'accounts/tipos/form.html'
    success_url = reverse_lazy('tipousuario_list')
    def test_func(self):
        return self.request.user.is_staff
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creado_por = self.request.user
        form.instance = obj
        return super().form_valid(form)

class TipoUsuarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TipoUsuario
    fields = ['nombre','descripcion']
    template_name = 'accounts/tipos/form.html'
    success_url = reverse_lazy('tipousuario_list')
    def test_func(self):
        return self.request.user.is_staff
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.actualizado_por = self.request.user
        form.instance = obj
        return super().form_valid(form)

class TipoUsuarioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TipoUsuario
    template_name = 'accounts/tipos/confirm_delete.html'
    success_url = reverse_lazy('tipousuario_list')
    def test_func(self):
        return self.request.user.is_staff

def _es_admin(user):
    if user.is_superuser or user.is_staff:
        return True
    try:
        perfil = user.perfil
    except PerfilUsuario.DoesNotExist:
        return False
    if perfil.tipo is None:
        return False
    return perfil.tipo.nombre.lower() == 'administrador'

class UserCreateWithRoleForm(UserCreationForm):
    tipo = forms.ModelChoiceField(queryset=TipoUsuario.objects.all(), required=False)
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username','first_name','last_name','email')
    def save(self, commit=True):
        user = super().save(commit=commit)
        tipo = self.cleaned_data.get('tipo')
        PerfilUsuario.objects.update_or_create(user=user, defaults={'tipo': tipo})
        return user

class UserUpdateWithRoleForm(UserChangeForm):
    password = None
    tipo = forms.ModelChoiceField(queryset=TipoUsuario.objects.all(), required=False)
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('username','first_name','last_name','email','is_active')
    def save(self, commit=True):
        user = super().save(commit=commit)
        tipo = self.cleaned_data.get('tipo')
        PerfilUsuario.objects.update_or_create(user=user, defaults={'tipo': tipo})
        return user

class UsuarioListView(LoginRequiredMixin, ListView):
    template_name = 'accounts/usuarios/list.html'
    context_object_name = 'usuarios'
    def get_queryset(self):
        return get_user_model().objects.all().order_by('username')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tipos'] = TipoUsuario.objects.all()
        ctx['puede_admin'] = _es_admin(self.request.user)
        return ctx

class UsuarioDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'accounts/usuarios/detail.html'

class UsuarioCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = UserCreateWithRoleForm
    template_name = 'accounts/usuarios/form.html'
    success_url = reverse_lazy('usuario_list')
    def test_func(self):
        return _es_admin(self.request.user)

class UsuarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateWithRoleForm
    template_name = 'accounts/usuarios/form.html'
    success_url = reverse_lazy('usuario_list')
    def test_func(self):
        return _es_admin(self.request.user)

class UsuarioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = get_user_model()
    template_name = 'accounts/usuarios/confirm_delete.html'
    success_url = reverse_lazy('usuario_list')
    def test_func(self):
        return _es_admin(self.request.user)
