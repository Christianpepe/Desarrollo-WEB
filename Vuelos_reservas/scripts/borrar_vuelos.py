# scripts/borrar_vuelos.py
import os
import sys
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from Vuelos_reservas.apps.vuelos.models import Vuelo

def borrar_vuelos():
    print("🗑️ Borrando todos los vuelos...")
    Vuelo.objects.all().delete()
    print("✅ Vuelos eliminados.")

if __name__ == '__main__':
    borrar_vuelos()
