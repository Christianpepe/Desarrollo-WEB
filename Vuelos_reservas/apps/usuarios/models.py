
# Este archivo define el modelo de usuario extendido para el sistema,
# agregando campos adicionales a los del usuario estándar de Django.


from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    """
    Modelo personalizado de usuario que extiende AbstractUser.
    Incluye campos adicionales como prioridad y teléfono.
    """
    prioridad = models.IntegerField(default=0, help_text="Nivel de prioridad del usuario (para upgrades, etc.)")
    telefono = models.CharField(max_length=15, blank=True, null=True, help_text="Teléfono de contacto del usuario")
