from django.db import models
from apps.pacientes.models import Paciente
from apps.especialidades.models import Especialidad
from apps.accounts.models import Medico
from django.utils import timezone

class CitaEcografia(models.Model):
    ESTADOS = (
        ('PROGRAMADA', 'Programada'),
        ('CANCELADA', 'Cancelada'),
        ('REPROGRAMADA', 'Reprogramada'),
        ('REALIZADA', 'Realizada'),
    )
    
    ESTADO_ATENCION = (
        ('EN_ESPERA', 'En Espera'),
        ('EN_ATENCION', 'En Atención'),
        ('ATENDIDO', 'Atendido'),
    )
    
    # Información del paciente y especialidad
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas_ecografia')
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name='citas_ecografia_medico')
    
    # Referencia a la cita original que generó esta ecografía
    cita_consulta = models.ForeignKey('citas.Cita', on_delete=models.SET_NULL, null=True, blank=True, related_name='citas_ecografia_generadas')
    
    # Médico que realiza la ecografía
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='citas_ecografia')
    
    # Información de fecha y hora
    fecha = models.DateField()
    hora = models.TimeField()
    
    # Información de la cita
    codigo = models.CharField(max_length=20, unique=True, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PROGRAMADA')
    
    # Información de atención
    estado_atencion = models.CharField(max_length=20, choices=ESTADO_ATENCION, default='EN_ESPERA')
    tiempo_inicio_atencion = models.DateTimeField(null=True, blank=True)
    tiempo_fin_atencion = models.DateTimeField(null=True, blank=True)
    duracion_atencion_minutos = models.IntegerField(null=True, blank=True)
    
    # Comentario del médico solicitante
    comentario_medico = models.TextField(null=True, blank=True)
    
    # Resultado de la ecografía
    resultado_ecografia = models.TextField(null=True, blank=True)
    
    # Auditoría
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha', '-hora']
        verbose_name = "Cita de Ecografía"
        verbose_name_plural = "Citas de Ecografía"
        constraints = [
            models.UniqueConstraint(fields=['medico', 'fecha', 'hora'], name='cita_eco_unica_por_medico_slot')
        ]
    
    def __str__(self):
        return f'{self.paciente} - {self.especialidad} - {self.fecha} {self.hora}'
    
    def calcular_duracion(self):
        """Calcula la duración de la atención en minutos"""
        if self.tiempo_inicio_atencion and self.tiempo_fin_atencion:
            diferencia = self.tiempo_fin_atencion - self.tiempo_inicio_atencion
            minutos = int(diferencia.total_seconds() / 60)
            return minutos
        return None
    
    def save(self, *args, **kwargs):
        """Sobrescribir save para calcular automáticamente la duración"""
        if self.tiempo_inicio_atencion and self.tiempo_fin_atencion and not self.duracion_atencion_minutos:
            self.duracion_atencion_minutos = self.calcular_duracion()
        super().save(*args, **kwargs)
