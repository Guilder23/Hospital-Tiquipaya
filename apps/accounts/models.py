# accounts/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200, blank=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tipousuario_creados',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    actualizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tipousuario_actualizados',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

# ------------------------
# PERFIL (Extiende a User)
# ------------------------
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")

    # Datos personales
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, null=True, blank=True)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=[('M','Masculino'), ('F','Femenino'), ('O','Otro')])
    direccion = models.CharField(max_length=255, blank=True, null=True)

    # Datos del CI
    ci = models.CharField(max_length=20, null=True, blank=True)
    complemento_ci = models.CharField(max_length=10, null=True, blank=True)
    expedido = models.CharField(max_length=5, default="CB")

    # Teléfonos
    telefono = models.CharField(max_length=15, null=True, blank=True)
    celular = models.CharField(max_length=15, null=True, blank=True)

    # Email
    correo = models.EmailField(max_length=150, null=True, blank=True)

    # Tipo / Rol
    tipo = models.ForeignKey(
        TipoUsuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno}"

# ------------------------
# MODELO MÉDICO
# ------------------------
class Medico(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='medico'
    )

    especialidad = models.ForeignKey('especialidades.Especialidad', on_delete=models.SET_NULL, null=True)
    nro_matricula = models.CharField(max_length=20)
    consultorio = models.CharField(max_length=50)

    turnos = models.ForeignKey("horarios.HorariosAtencion", on_delete=models.SET_NULL, null=True)
    dias_atencion = models.ForeignKey("horarios.DiasAtencion", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.perfil.nombres} {self.user.perfil.apellido_paterno}"


# ------------------------
# MODELO ADMISIÓN
# ------------------------
class Admision(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admision")
    ventanilla = models.CharField(max_length=20)
    turnos = models.ForeignKey("horarios.HorariosAtencion", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Admisión - {self.user.username}"


# ------------------------
# MODELO ENCARGADO DE ADMISIÓN
# ------------------------
class EncargadoAdmision(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="encargado_admision")
    ventanilla = models.CharField(max_length=20)
    turnos = models.ForeignKey("horarios.HorariosAtencion", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Encargado Admisión - {self.user.username}"
