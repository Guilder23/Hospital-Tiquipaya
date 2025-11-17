from django.urls import path
from .views import (
    register,
    TipoUsuarioListView, TipoUsuarioCreateView, TipoUsuarioUpdateView, TipoUsuarioDeleteView,
    UsuarioListView, UsuarioDetailView, UsuarioCreateView, UsuarioUpdateView, UsuarioDeleteView,
)
urlpatterns = [
    path('register/', register, name='register'),
    # Tipos de Usuario
    path('tipos/', TipoUsuarioListView.as_view(), name='tipousuario_list'),
    path('tipos/nuevo/', TipoUsuarioCreateView.as_view(), name='tipousuario_create'),
    path('tipos/<int:pk>/editar/', TipoUsuarioUpdateView.as_view(), name='tipousuario_update'),
    path('tipos/<int:pk>/eliminar/', TipoUsuarioDeleteView.as_view(), name='tipousuario_delete'),
    # Usuarios
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/nuevo/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/<int:pk>/', UsuarioDetailView.as_view(), name='usuario_detail'),
    path('usuarios/<int:pk>/editar/', UsuarioUpdateView.as_view(), name='usuario_update'),
    path('usuarios/<int:pk>/eliminar/', UsuarioDeleteView.as_view(), name='usuario_delete'),
]