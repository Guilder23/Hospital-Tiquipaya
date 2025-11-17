from django.db import models
class Medico(models.Model):
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)
    def __str__(self):
        return f'{self.apellidos} {self.nombres}'