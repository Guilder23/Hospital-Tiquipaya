from django.urls import path
from .views import TurnoListView, TurnoDetailView, TurnoCreateView

app_name = 'turnos'

urlpatterns = [
    path('', TurnoListView.as_view(), name='lista'),
    path('nuevo/', TurnoCreateView.as_view(), name='crear'),
    path('<int:pk>/', TurnoDetailView.as_view(), name='detalle'),
]