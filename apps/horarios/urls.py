# horarios/urls.py (Actualizado)

from django.urls import path
# Importar la nueva vista API y las vistas de plantilla
from .views import TurnoListView, TurnoAPIView 

app_name = 'turnos'

urlpatterns = [
    # Ruta principal para la plantilla de la lista
    path('', TurnoListView.as_view(), name='lista'),

    # Rutas API para manejar POST, PATCH, DELETE desde los modales JS
    path('api/', TurnoAPIView.as_view(), name='api-list-create'), # GET, POST
    path('api/<int:pk>/', TurnoAPIView.as_view(), name='api-detail-update-delete'), # GET(id), PATCH, DELETE
    
    # La ruta de detalle se mantiene aunque la usemos menos con el modal
    # path('<int:pk>/', TurnoDetailView.as_view(), name='detalle'),
]