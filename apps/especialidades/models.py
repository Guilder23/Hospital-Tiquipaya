from django.db import models
class Especialidad(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    cupo_diario = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.nombre