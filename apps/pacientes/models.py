from django.db import models
class Paciente(models.Model):
    ci = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    def __str__(self):
        return f'{self.apellidos} {self.nombres} ({self.ci})'