from django.db import models
import uuid


class Ecografia(models.Model):
    ESTADOS = (
        ('ACTIVA', 'Activa'),
        ('INACTIVA', 'Inactiva'),
    )

    medico = models.ForeignKey('accounts.Medico', on_delete=models.CASCADE, related_name='ecografias')
    especialidad = models.ForeignKey('especialidades.Especialidad', on_delete=models.CASCADE)
    
    nombre = models.CharField(max_length=150, default="Ecografía")
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ACTIVA')
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Ecografía'
        verbose_name_plural = 'Ecografías'

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'
    
    def generar_codigo(self):
        """Genera un código único ECOxxxxxxx"""
        self.codigo = f"ECO{uuid.uuid4().hex[:6].upper()}"
        while Ecografia.objects.filter(codigo=self.codigo).exists():
            self.codigo = f"ECO{uuid.uuid4().hex[:6].upper()}"
        return self.codigo
