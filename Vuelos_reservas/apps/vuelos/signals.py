from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.vuelos.models import Vuelo
from apps.vuelos.utils import generar_asientos_para_vuelo

@receiver(post_save, sender=Vuelo)
def crear_asientos_automaticamente(sender, instance, created, **kwargs):
    if created:
        generar_asientos_para_vuelo(instance)
