from django.db import models
from apps.usuarios.models import Usuario
from apps.reservas.models import Reserva

class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    asunto = models.CharField(max_length=100)
    mensaje = models.TextField()
    enviado = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    email_destinatario = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
