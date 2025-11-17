from django.contrib import admin
from .models import Especialidad
@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre','cupo_diario')
    search_fields = ('nombre',)