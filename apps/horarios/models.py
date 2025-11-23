from django.db import models

class DiasAtencion(models.Model):
    lunes = models.BooleanField(default=False)
    martes = models.BooleanField(default=False)
    miercoles = models.BooleanField(default=False)
    jueves = models.BooleanField(default=False)
    viernes = models.BooleanField(default=False)

    def __str__(self):
        return f"Días: {self.lunes}{self.martes}{self.miercoles}{self.jueves}{self.viernes}"
    
class HorariosAtencion(models.Model):
    madrugue = models.BooleanField(default=False)
    mannana = models.BooleanField(default=False)
    tarde = models.BooleanField(default=False)
    noche = models.BooleanField(default=False)

    def __str__(self):
        return f"Horarios: {self.madrugue}{self.mannana}{self.tarde}{self.noche}"