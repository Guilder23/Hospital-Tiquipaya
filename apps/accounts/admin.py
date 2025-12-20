from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import TipoUsuario, Medico, Admision, EncargadoAdmision, Ecografo, Perfil

@admin.register(TipoUsuario)
class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre','descripcion')
    search_fields = ('nombre',)

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo', 'nombres', 'apellido_paterno')
    search_fields = ('user__username', 'nombres', 'apellido_paterno')
    list_filter = ('tipo',)

# Extender el UserAdmin de Django para permitir crear usuarios desde el admin
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    fields = ('tipo', 'nombres', 'apellidos', 'genero', 'fecha_nacimiento', 'fotografia')

class CustomUserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        return fieldsets

# Reemplazar el UserAdmin por defecto
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

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