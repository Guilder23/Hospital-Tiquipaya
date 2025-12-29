from django.contrib import admin
from .models import DiasAtencion, Turnos

admin.site.register(DiasAtencion)

@admin.register(Turnos)
class TurnosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'hora_ini', 'hora_fin', 'estado')
    list_filter = ('estado',)
    search_fields = ('nombre',)