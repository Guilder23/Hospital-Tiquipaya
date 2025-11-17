from django.db import models
from apps.especialidades.models import Especialidad
from apps.medicos.models import Medico
class Horario(models.Model):
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True, blank=True)
    dia_semana = models.IntegerField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    duracion_minutos = models.PositiveIntegerField(default=20)
    def __str__(self):
        return f'{self.especialidad} {self.dia_semana} {self.hora_inicio}-{self.hora_fin}'