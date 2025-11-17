from django.db import models
from apps.pacientes.models import Paciente
from apps.especialidades.models import Especialidad
class Cita(models.Model):
    ESTADOS = (
        ('PROGRAMADA','PROGRAMADA'),
        ('CANCELADA','CANCELADA'),
        ('REPROGRAMADA','REPROGRAMADA'),
    )
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PROGRAMADA')
    creada_en = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = (('paciente','fecha'),)
    def __str__(self):
        return f'{self.paciente} {self.especialidad} {self.fecha} {self.hora}'