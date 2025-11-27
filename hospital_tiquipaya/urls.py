from django.contrib import admin
from django.urls import path, include
from apps.citas import views as citas_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', citas_views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('especialidades/', include('apps.especialidades.urls')),
    path('pacientes/', include('apps.pacientes.urls')),
    path('citas/', include('apps.citas.urls')),
    path('ecografias/', include('apps.ecografias.urls')),
    path('turnos/', include('apps.horarios.urls', namespace='turnos')),
]
