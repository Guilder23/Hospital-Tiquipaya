from django.db import models
from django.conf import settings
class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tipousuario_creados',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    actualizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tipousuario_actualizados',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['nombre']
    def __str__(self):
        return self.nombre

class PerfilUsuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f'{self.user.username} - {self.tipo.nombre if self.tipo else "Sin tipo"}'
