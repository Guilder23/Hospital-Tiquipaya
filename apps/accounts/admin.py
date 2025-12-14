from django.contrib import admin
from .models import TipoUsuario, Medico, Admision, EncargadoAdmision, Ecografo

@admin.register(TipoUsuario)
class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre','descripcion')
    search_fields = ('nombre',)

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'especialidad', 'nro_matricula')
    search_fields = ('user__perfil__nombres',)

@admin.register(Admision)
class AdmisionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'ventanilla')
    search_fields = ('user__username',)

@admin.register(EncargadoAdmision)
class EncargadoAdmisionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'ventanilla')
    search_fields = ('user__username',)

@admin.register(Ecografo)
class EcografoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'nro_matricula', 'consultorio')
    search_fields = ('user__perfil__nombres',)
    filter_horizontal = ('ecografias', 'turnos')

