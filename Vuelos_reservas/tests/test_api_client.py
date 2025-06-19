# tests/test_api_client.py

import sys
import os

# Añadir la ruta raíz del proyecto para que pueda encontrar 'apps'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apps.api_integration.api_client import get_flights_by_date_range

if __name__ == '__main__':
    vuelos = get_flights_by_date_range()
    print(f"Vuelos encontrados: {len(vuelos)}")
    for vuelo in vuelos[:3]:
        airline = vuelo.get('airline', {}).get('name', 'Desconocida')
        flight_code = vuelo.get('flight', {}).get('iata', 'N/A')
        status = vuelo.get('flight_status', 'Sin estado')
        print(f"{airline} - {flight_code} - {status}")

# Este script se ejecuta directamente para probar la funcionalidad de obtener vuelos
# desde la API de Aviationstack.