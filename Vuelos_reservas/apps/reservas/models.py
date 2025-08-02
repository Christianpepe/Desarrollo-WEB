from django.db import models
from Vuelos_reservas.apps.usuarios.models import Usuario
from Vuelos_reservas.apps.vuelos.models import Vuelo, Asiento
#CORONA GARCIA CHRISTIAN JAVIER
class Reserva(models.Model):
    codigo_reserva = models.CharField(max_length=10, unique=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, default="pendiente")  # o confirmada/cancelada
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField(null=True, blank=True)
    pasajeros_total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Pasajero(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    asiento = models.ForeignKey(Asiento, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_completo = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=30)
    numero_documento = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField()
    nacionalidad = models.CharField(max_length=50)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    equipaje_adicional = models.BooleanField(default=False)
    comida_especial = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
