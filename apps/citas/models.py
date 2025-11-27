from django.db import models
from django.utils import timezone
from apps.pacientes.models import Paciente
from apps.especialidades.models import Especialidad
import uuid

class Cita(models.Model):
    ESTADOS = (
        ('PROGRAMADA','PROGRAMADA'),
        ('CANCELADA','CANCELADA'),
        ('REPROGRAMADA','REPROGRAMADA'),
    )
    
    ESTADO_ATENCION = (
        ('EN_ESPERA', 'En Espera'),
        ('EN_ATENCION', 'En Atención'),
        ('ATENDIDO', 'Atendido'),
    )
    
    TIPO_CITA = (
        ('CONSULTA', 'Consulta'),
        ('ECOGRAFIA', 'Ecografía'),
    )
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    medico = models.ForeignKey('accounts.Medico', on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    codigo = models.CharField(max_length=20, unique=True, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PROGRAMADA')
    tipo_cita = models.CharField(max_length=20, choices=TIPO_CITA, default='CONSULTA')
    
    # Campos para rastrear atención
    estado_atencion = models.CharField(max_length=20, choices=ESTADO_ATENCION, default='EN_ESPERA')
    tiempo_inicio_atencion = models.DateTimeField(null=True, blank=True)
    tiempo_fin_atencion = models.DateTimeField(null=True, blank=True)
    duracion_atencion_minutos = models.IntegerField(null=True, blank=True)
    
    # Campo para ecografía
    requiere_ecografia = models.BooleanField(default=False)
    
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['medico','fecha','hora'], name='cita_unica_por_medico_slot')
        ]

    def __str__(self):
        return f'{self.paciente} {self.especialidad} {self.fecha} {self.hora}'
    
    def calcular_duracion(self):
        """Calcula la duración de la atención en minutos"""
        if self.tiempo_inicio_atencion and self.tiempo_fin_atencion:
            diferencia = self.tiempo_fin_atencion - self.tiempo_inicio_atencion
            minutos = int(diferencia.total_seconds() / 60)
            return minutos
        return None
