from django.contrib import admin
from .models import Cita
@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente','especialidad','fecha','hora','estado')
    list_filter = ('especialidad','fecha','estado')
    search_fields = ('paciente__ci','paciente__apellidos','paciente__nombres')