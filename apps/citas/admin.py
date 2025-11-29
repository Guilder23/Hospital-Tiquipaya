from django.contrib import admin
from .models import Cita

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'paciente', 'especialidad', 'medico', 'fecha', 'hora', 'estado', 'estado_atencion', 'tipo_cita')
    list_filter = ('especialidad', 'fecha', 'estado', 'estado_atencion', 'tipo_cita')
    search_fields = ('paciente__ci', 'paciente__nombres', 'paciente__apellidos', 'codigo')
    readonly_fields = ('codigo', 'creada_en', 'duracion_atencion_minutos', 'tiempo_inicio_atencion', 'tiempo_fin_atencion')
    
    fieldsets = (
        ('Información General', {
            'fields': ('codigo', 'paciente', 'especialidad', 'medico', 'tipo_cita')
        }),
        ('Fechas y Horas', {
            'fields': ('fecha', 'hora', 'creada_en')
        }),
        ('Estado de la Cita', {
            'fields': ('estado', 'estado_atencion')
        }),
        ('Control de Atención', {
            'fields': ('tiempo_inicio_atencion', 'tiempo_fin_atencion', 'duracion_atencion_minutos'),
            'classes': ('collapse',)
        }),
        ('Servicios Adicionales', {
            'fields': ('requiere_ecografia',),
            'classes': ('collapse',)
        }),
    )