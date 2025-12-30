from django.db import models
from django.contrib.auth.models import User

class DiasAtencion(models.Model):
    lunes = models.BooleanField(default=False)
    martes = models.BooleanField(default=False)
    miercoles = models.BooleanField(default=False)
    jueves = models.BooleanField(default=False)
    viernes = models.BooleanField(default=False)
    sabado = models.BooleanField(default=False)
    domingo = models.BooleanField(default=False)

    def __str__(self):
        dias = []

        if self.lunes: dias.append("Lunes")
        if self.martes: dias.append("Martes")
        if self.miercoles: dias.append("Miércoles")
        if self.jueves: dias.append("Jueves")
        if self.viernes: dias.append("Viernes")
        if self.sabado: dias.append("Sábado")
        if self.domingo: dias.append("Domingo")

        return ", ".join(dias) if dias else "Sin días asignados"
    

# Modelo global para horario del sistema de citas
class HorarioSistema(models.Model):
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    actualizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Horario: {self.hora_inicio} - {self.hora_fin}"

    class Meta:
        verbose_name = "Horario del sistema de citas"
        verbose_name_plural = "Horarios del sistema de citas"
    
class Turnos(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    hora_ini = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre