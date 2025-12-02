from django.urls import path
from .views import ContratoListView, ContratoAPIView

app_name = 'contratos'

urlpatterns = [
    path('', ContratoListView.as_view(), name='list'),
    path('api/', ContratoAPIView.as_view(), name='api'),
    path('api/<int:pk>/', ContratoAPIView.as_view(), name='api_detail'),
]

