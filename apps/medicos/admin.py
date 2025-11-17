from django.contrib import admin
from .models import Medico
@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('apellidos','nombres')
    search_fields = ('apellidos','nombres')