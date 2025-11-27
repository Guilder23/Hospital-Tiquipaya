from django.contrib import admin
from .models import Ecografia


@admin.register(Ecografia)
class EcografiaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'medico', 'especialidad', 'estado', 'fecha_creacion')
    list_filter = ('especialidad', 'estado', 'fecha_creacion', 'medico')
    search_fields = ('codigo', 'nombre', 'medico__user__first_name')
    readonly_fields = ('codigo', 'fecha_creacion', 'fecha_actualizacion')
    
    fieldsets = (
        ('Información General', {
            'fields': ('codigo', 'nombre', 'medico', 'especialidad')
        }),
        ('Detalles', {
            'fields': ('descripcion', 'estado')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.codigo:
            obj.generar_codigo()
        super().save_model(request, obj, form, change)
