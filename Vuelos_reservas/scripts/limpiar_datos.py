#scripts/limpiar_datos.py
import os
import sys
import django


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#Configura el entorno Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.vuelos.models import Vuelo, Aeropuerto, Aerolinea, ModeloAvion, Asiento
from apps.reservas.models import Reserva, Pasajero
from apps.notificaciones.models import Notificacion

def limpiar_datos():
    print("🚨 Iniciando limpieza de datos...")

    # Orden correcta por dependencias
    try:
        print("🗑️ Eliminando notificaciones...")
        Notificacion.objects.all().delete()
    except Exception as e:
        print(f"⚠️ No se pudo eliminar notificaciones: {e}")

    try:
        print("🗑️ Eliminando pasajeros...")
        Pasajero.objects.all().delete()
    except Exception as e:
        print(f"⚠️ No se pudo eliminar pasajeros: {e}")

    try:
        print("🗑️ Eliminando reservas...")
        Reserva.objects.all().delete()
    except Exception as e:
        print(f"⚠️ No se pudo eliminar reservas: {e}")

    try:
        print("🗑️ Eliminando asientos...")
        Asiento.objects.all().delete()
    except Exception as e:
        print(f"⚠️ No se pudo eliminar asientos: {e}")

    try:
        print("🗑️ Eliminando vuelos...")
        Vuelo.objects.all().delete()
    except Exception as e:
        print(f"⚠️ No se pudo eliminar vuelos: {e}")

    try:
        print("🗑️ Eliminando modelos de avión...")
        ModeloAvion.objects.all().delete()
    except Exception as e:
        print(f"⚠️ No se pudo eliminar modelos de avión: {e}")

    try:
        print("🗑️ Eliminando aerolíneas...")
        Aerolinea.objects.all().delete()
    except Exception as e:
        print(f"⚠️ No se pudo eliminar aerolíneas: {e}")

    try:
        print("🗑️ Eliminando aeropuertos...")
        Aeropuerto.objects.all().delete()
    except Exception as e:
        print(f"⚠️ No se pudo eliminar aeropuertos: {e}")

    print("✅ Limpieza completada.")

if __name__ == "__main__":
    limpiar_datos()