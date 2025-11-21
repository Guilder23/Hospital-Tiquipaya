from django.contrib import admin
from .models import Paciente
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('ci','apellido_paterno','apellido_materno','nombres','celular','activo')
    search_fields = ('ci','apellido_paterno','apellido_materno','nombres','celular')