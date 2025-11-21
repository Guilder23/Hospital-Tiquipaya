from django.db import models
class Paciente(models.Model):
    GENEROS = (
        ('M','Masculino'),
        ('F','Femenino'),
    )
    EXPEDIDOS = (
        ('LP','La Paz'),('SC','Santa Cruz'),('CB','Cochabamba'),('OR','Oruro'),('PT','Potosí'),('TJ','Tarija'),('CH','Chuquisaca'),('BE','Beni'),('PA','Pando')
    )
    ci = models.CharField(max_length=20, unique=True)
    expedido = models.CharField(max_length=2, choices=EXPEDIDOS, blank=True)
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENEROS, blank=True)
    nacionalidad = models.CharField(max_length=60, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    tiene_seguro = models.BooleanField(default=False)
    numero_seguro = models.CharField(max_length=60, blank=True)
    emergencia_nombre = models.CharField(max_length=120, blank=True)
    emergencia_telefono = models.CharField(max_length=30, blank=True)
    emergencia_relacion = models.CharField(max_length=60, blank=True)
    def __str__(self):
        return f'{self.apellidos} {self.nombres} ({self.ci})'