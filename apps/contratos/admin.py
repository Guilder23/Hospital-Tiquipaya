from django.contrib import admin
from .models import Contrato

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('nombre','fecha_inicio','fecha_fin','estado','creado_en','actualizado_en')
    list_filter = ('estado',)
    search_fields = ('nombre',)

