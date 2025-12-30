from django.contrib import admin
from .models import DiasAtencion, Turnos, HorarioSistema

admin.site.register(DiasAtencion)

@admin.register(Turnos)
class TurnosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'hora_ini', 'hora_fin', 'estado')
    list_filter = ('estado',)
    search_fields = ('nombre',)

@admin.register(HorarioSistema)
class HorarioSistemaAdmin(admin.ModelAdmin):
    list_display = ('hora_inicio', 'hora_fin', 'actualizado_por', 'actualizado_en')
    readonly_fields = ('actualizado_en',)