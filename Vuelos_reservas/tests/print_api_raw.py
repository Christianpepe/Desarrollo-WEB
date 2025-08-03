import sys
import os
import json
from datetime import datetime

# Añadir la ruta raíz del proyecto para que pueda encontrar 'apps'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Vuelos_reservas.apps.api_integration.api_client import get_real_time_flights

if __name__ == '__main__':
    # Puedes cambiar la fecha y el ICAO según lo que quieras probar
    fecha = datetime.now().date()
    icao = 'MMMX'  # Cambia por el ICAO que quieras probar
    vuelos = get_real_time_flights(fecha, origen_icao=icao)
    # Imprime cada vuelo en crudo, uno por uno, para fácil inspección
    for idx, vuelo in enumerate(vuelos):
        print(f"--- Vuelo #{idx+1} ---")
        print(json.dumps(vuelo, indent=2, ensure_ascii=False))
        print("\n")
