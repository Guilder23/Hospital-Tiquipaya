from django.db import models

class DiasAtencion(models.Model):
    lunes = models.BooleanField(default=False)
    martes = models.BooleanField(default=False)
    miercoles = models.BooleanField(default=False)
    jueves = models.BooleanField(default=False)
    viernes = models.BooleanField(default=False)

    def __str__(self):
        dias = []

        if self.lunes: dias.append("Lunes")
        if self.martes: dias.append("Martes")
        if self.miercoles: dias.append("Miércoles")
        if self.jueves: dias.append("Jueves")
        if self.viernes: dias.append("Viernes")

        return ", ".join(dias) if dias else "Sin días asignados"
    
class HorariosAtencion(models.Model):
    madrugue = models.BooleanField(default=False)
    mannana = models.BooleanField(default=False)
    tarde = models.BooleanField(default=False)
    noche = models.BooleanField(default=False)

    def __str__(self):
        horas = []

        if self.madrugue: horas.append("madrugue")
        if self.mannana: horas.append("mañana")
        if self.tarde: horas.append("tarde")
        if self.noche: horas.append("noche")

        return ", ".join(horas) if horas else "Sin días asignados"