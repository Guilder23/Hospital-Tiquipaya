from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/data/', views.get_dashboard_data, name='get_data'),
]
