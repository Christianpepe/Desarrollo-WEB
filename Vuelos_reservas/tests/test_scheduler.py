import os
import sys
import django

# Asegura que el path base esté en sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configura el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.api_integration.scheduler import ejecutar_carga_completa

print("Iniciando test de carga de vuelos simulados y reales (AeroDataBox)...")
ejecutar_carga_completa(cargar_reales=True, cargar_simulados=False, icao_code='KLAX')  # Cambia 'KLAX' por el ICAO que desees probar
