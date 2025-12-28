from django.db import models
from django.utils import timezone
from django.conf import settings
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
    
    # Campos para ecografía
    requiere_ecografia = models.BooleanField(default=False)
    ecografia = models.ForeignKey('ecografias.Ecografia', on_delete=models.SET_NULL, null=True, blank=True, related_name='citas_solicitadas')
    comentario_ecografia = models.TextField(null=True, blank=True)
    
    # Auditoría: quién creó la cita
    usuario_creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='citas_creadas')
    
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
            total_segundos = int(diferencia.total_seconds())
            minutos = total_segundos // 60
            # Retornar al menos 1 si hay algún segundo transcurrido
            if minutos == 0 and total_segundos > 0:
                return 1  # Mínimo 1 minuto si hubo tiempo transcurrido
            return minutos if minutos > 0 else None
        return None
    
    def get_duracion_formateada(self):
        """Retorna la duración en formato legible (ej: '5 min' o '1h 30min')"""
        if self.tiempo_inicio_atencion and self.tiempo_fin_atencion:
            diferencia = self.tiempo_fin_atencion - self.tiempo_inicio_atencion
            total_segundos = int(diferencia.total_seconds())
            
            if total_segundos < 60:
                return f"{total_segundos} seg"
            
            minutos = total_segundos // 60
            segundos = total_segundos % 60
            
            if minutos < 60:
                if segundos > 0:
                    return f"{minutos}:{segundos:02d} min"
                return f"{minutos} min"
            
            horas = minutos // 60
            mins_restantes = minutos % 60
            return f"{horas}h {mins_restantes}min"
        return None
    
    def save(self, *args, **kwargs):
        """Sobrescribir save para calcular automáticamente la duración"""
        if self.tiempo_inicio_atencion and self.tiempo_fin_atencion and not self.duracion_atencion_minutos:
            self.duracion_atencion_minutos = self.calcular_duracion()
        super().save(*args, **kwargs)
