from django.contrib import admin
from .models import CitaEcografia


@admin.register(CitaEcografia)
class CitaEcografiaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'especialidad', 'medico', 'fecha', 'hora', 'estado', 'estado_atencion')
    list_filter = ('especialidad', 'fecha', 'estado', 'estado_atencion', 'medico')
    search_fields = ('paciente__nombres', 'paciente__apellido_paterno', 'paciente__ci')
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información de Paciente', {
            'fields': ('paciente', 'especialidad', 'cita_consulta')
        }),
        ('Información de Médico', {
            'fields': ('medico',)
        }),
        ('Fecha y Hora', {
            'fields': ('fecha', 'hora', 'codigo')
        }),
        ('Estado', {
            'fields': ('estado', 'estado_atencion')
        }),
        ('Tiempo de Atención', {
            'fields': ('tiempo_inicio_atencion', 'tiempo_fin_atencion', 'duracion_atencion_minutos')
        }),
        ('Información Médica', {
            'fields': ('comentario_medico', 'resultado_ecografia')
        }),
        ('Auditoría', {
            'fields': ('creada_en', 'actualizada_en'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('creada_en', 'actualizada_en', 'duracion_atencion_minutos')
