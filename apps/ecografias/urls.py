from django.urls import path
from .views import EcografiaListView, EcografiaCreateView, EcografiaUpdateView, EcografiaDeleteView

urlpatterns = [
    path('', EcografiaListView.as_view(), name='ecografia_list'),
    path('nuevo/', EcografiaCreateView.as_view(), name='ecografia_create'),
    path('<int:pk>/editar/', EcografiaUpdateView.as_view(), name='ecografia_update'),
    path('<int:pk>/eliminar/', EcografiaDeleteView.as_view(), name='ecografia_delete'),
]
