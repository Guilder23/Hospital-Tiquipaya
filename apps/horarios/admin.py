from django.contrib import admin
from .models import Horario
@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('especialidad','medico','dia_semana','hora_inicio','hora_fin','duracion_minutos')
    list_filter = ('especialidad','dia_semana')