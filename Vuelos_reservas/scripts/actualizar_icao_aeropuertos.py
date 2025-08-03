# scripts/actualizar_icao_aeropuertos.py
import os
import sys
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from Vuelos_reservas.apps.vuelos.models import Aeropuerto

# Diccionario: codigo_iata -> codigo_icao
IATA_ICAO = {
    'KDFW': 'DFW',   # Dallas-Fort Worth
    'MMMX': 'MMMX',  # Mexico City
    'MMTJ': 'MMTJ',  # Tijuana
    'KIAH': 'IAH',   # Houston
    'MMUN': 'MMUN',  # Cancún
    'KMDW': 'MDW',   # Chicago Midway
    'KLAX': 'LAX',   # Los Angeles
    'MMAS': 'MMAS',  # Aguascalientes
}

def actualizar_icao():
    print('Actualizando codigo_icao de aeropuertos...')
    for aeropuerto in Aeropuerto.objects.all():
        iata = aeropuerto.codigo_iata
        icao = IATA_ICAO.get(iata)
        if icao:
            aeropuerto.codigo_icao = icao
            aeropuerto.save()
            print(f'✔️ {iata} -> {icao}')
        else:
            print(f'⚠️ No se encontró ICAO para {iata}')
    print('✅ Actualización finalizada.')

if __name__ == '__main__':
    actualizar_icao()
