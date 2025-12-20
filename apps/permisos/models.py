from django.db import models
from django.contrib.auth.models import User
from apps.accounts.models import TipoUsuario


class Modulo(models.Model):
    """Módulos/opciones del sidebar del sistema"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    icono = models.CharField(max_length=50, blank=True, null=True, help_text="Clase CSS del ícono (ej: fas fa-users)")
    url = models.CharField(max_length=200, help_text="URL del módulo (ej: /pacientes/)")
    orden = models.IntegerField(default=0, help_text="Orden de aparición en el sidebar")
    activo = models.BooleanField(default=True)
    asignable = models.BooleanField(default=True, help_text="Si se puede asignar en la gestión de permisos")
    modulo_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='submodulos')
    # Roles que tienen este módulo por defecto (no se puede quitar, solo asignar permisos)
    roles_por_defecto = models.ManyToManyField(TipoUsuario, blank=True, related_name='modulos_por_defecto', help_text="Roles que tienen este módulo por defecto")
    
    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['orden', 'nombre']
    
    def __str__(self):
        if self.modulo_padre:
            return f"{self.modulo_padre.nombre} → {self.nombre}"
        return self.nombre


class Permiso(models.Model):
    """Permisos asignados a cada tipo de usuario por módulo"""
    TIPO_PERMISO = [
        ('sin_acceso', 'Sin Acceso'),
        ('solo_vista', 'Solo Vista'),
        ('editor', 'Editor'),
    ]
    
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE, related_name='permisos')
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='permisos')
    tipo_permiso = models.CharField(max_length=20, choices=TIPO_PERMISO, default='sin_acceso')
    visible = models.BooleanField(default=False, help_text="Si aparece en el sidebar")
    
    class Meta:
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'
        unique_together = ('tipo_usuario', 'modulo')
        ordering = ['tipo_usuario', 'modulo__orden']
    
    def __str__(self):
        return f"{self.tipo_usuario.nombre} - {self.modulo.nombre}: {self.get_tipo_permiso_display()}"
    
    def tiene_acceso(self):
        """Verifica si tiene algún tipo de acceso"""
        return self.visible and self.tipo_permiso != 'sin_acceso'
    
    def puede_editar(self):
        """Verifica si puede crear/editar/eliminar"""
        return self.visible and self.tipo_permiso == 'editor'
    
    def es_solo_vista(self):
        """Verifica si solo puede ver"""
        return self.visible and self.tipo_permiso == 'solo_vista'
