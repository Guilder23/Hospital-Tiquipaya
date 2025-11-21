from django.contrib import admin
from .models import Especialidad

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'created_at')
    list_filter = ('estado',)
    search_fields = ('nombre',)
