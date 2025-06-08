from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    prioridad = models.IntegerField(default=0)
    telefono = models.CharField(max_length=15, blank=True, null=True)
