from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from apps.citas import views as citas_views
from apps.accounts.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', citas_views.home, name='home'),
    path('dashboard/', include('apps.dashboard.urls')),
    # Custom login with role-based redirect
    path('accounts/login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('especialidades/', include('apps.especialidades.urls')),
    path('pacientes/', include('apps.pacientes.urls')),
    path('citas/', include('apps.citas.urls')),
    path('ecografias/', include('apps.ecografias.urls')),
    path('citas-ecografia/', include('apps.citas_ecografia.urls')),
    path('turnos/', include('apps.horarios.urls', namespace='turnos')),
    path('contratos/', include('apps.contratos.urls', namespace='contratos')),
    path('permisos/', include('apps.permisos.urls', namespace='permisos')),
]
