from django.db import models
from datetime import date

class Paciente(models.Model):
    GENEROS = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    )
    EXPEDIDOS = (
        ('LP', 'La Paz'), ('SC', 'Santa Cruz'), ('CB', 'Cochabamba'), ('OR', 'Oruro'), ('PT', 'Potosí'), ('TJ', 'Tarija'), ('CH', 'Chuquisaca'), ('BE', 'Beni'), ('PA', 'Pando')
    )

    nombres = models.CharField(max_length=120)
    apellido_paterno = models.CharField(max_length=120)
    apellido_materno = models.CharField(max_length=120, blank=True)

    ci = models.CharField(max_length=20, unique=True)
    ci_complemento = models.CharField(max_length=10, blank=True)
    expedido = models.CharField(max_length=2, choices=EXPEDIDOS, blank=True)

    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENEROS, blank=True)

    telefono_fijo = models.CharField(max_length=30, blank=True)
    celular = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    zona = models.CharField(max_length=100, blank=True)
    calle = models.CharField(max_length=120, blank=True)
    numero_domicilio = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=200, blank=True)

    nacionalidad = models.CharField(max_length=60, blank=True)

    tiene_seguro = models.BooleanField(default=False)
    numero_seguro = models.CharField(max_length=60, blank=True)

    emergencia_nombre = models.CharField(max_length=120, blank=True)
    emergencia_telefono = models.CharField(max_length=30, blank=True)
    emergencia_relacion = models.CharField(max_length=60, blank=True)

    activo = models.BooleanField(default=True)
    registrado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.apellido_paterno} {self.apellido_materno} {self.nombres} ({self.ci})'
    
    def get_edad(self):
        """Calcula la edad del paciente"""
        if self.fecha_nacimiento:
            hoy = date.today()
            edad = hoy.year - self.fecha_nacimiento.year
            if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
                edad -= 1
            return edad
        return None