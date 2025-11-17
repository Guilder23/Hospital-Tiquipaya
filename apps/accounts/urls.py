from django.urls import path
from .views import register, TipoUsuarioListView, TipoUsuarioCreateView, TipoUsuarioUpdateView, TipoUsuarioDeleteView
urlpatterns = [
    path('register/', register, name='register'),
    path('tipos/', TipoUsuarioListView.as_view(), name='tipousuario_list'),
    path('tipos/nuevo/', TipoUsuarioCreateView.as_view(), name='tipousuario_create'),
    path('tipos/<int:pk>/editar/', TipoUsuarioUpdateView.as_view(), name='tipousuario_update'),
    path('tipos/<int:pk>/eliminar/', TipoUsuarioDeleteView.as_view(), name='tipousuario_delete'),
]