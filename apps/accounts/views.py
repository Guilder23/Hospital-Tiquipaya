from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import TipoUsuario
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
