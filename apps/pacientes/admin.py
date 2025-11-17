from django.contrib import admin
from .models import Paciente
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('ci','apellidos','nombres','telefono')
    search_fields = ('ci','apellidos','nombres')