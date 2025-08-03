# scripts/limpiar_duplicados_icao.py
import os
import sys
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from Vuelos_reservas.apps.vuelos.models import Aeropuerto

def limpiar_duplicados_icao():
    print("Buscando duplicados de codigo_icao...")
    vistos = set()
    for aeropuerto in Aeropuerto.objects.all().order_by('id'):
        if aeropuerto.codigo_icao and aeropuerto.codigo_icao in vistos:
            print(f"Eliminando duplicado: {aeropuerto.codigo_icao} (id={aeropuerto.id})")
            aeropuerto.delete()
        else:
            vistos.add(aeropuerto.codigo_icao)
    print("✅ Duplicados eliminados.")

if __name__ == '__main__':
    limpiar_duplicados_icao()
