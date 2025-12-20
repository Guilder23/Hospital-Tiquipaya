from django.contrib import admin
from .models import Modulo, Permiso


class PermisoInline(admin.TabularInline):
    model = Permiso
    extra = 0
    fields = ('modulo', 'visible', 'tipo_permiso')


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'url', 'icono', 'orden', 'modulo_padre', 'activo')
    list_filter = ('activo', 'modulo_padre')
    search_fields = ('nombre', 'url')
    ordering = ('orden', 'nombre')


@admin.register(Permiso)
class PermisoAdmin(admin.ModelAdmin):
    list_display = ('tipo_usuario', 'modulo', 'tipo_permiso', 'visible')
    list_filter = ('tipo_permiso', 'visible', 'tipo_usuario')
    search_fields = ('tipo_usuario__nombre', 'modulo__nombre')
    ordering = ('tipo_usuario__nombre', 'modulo__orden')
