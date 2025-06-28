import requests
from datetime import datetime
from decouple import config

# Configuración
RAPIDAPI_KEY = config("RAPIDAPI_KEY")  # clave desde .env
RAPIDAPI_HOST = "aerodatabox.p.rapidapi.com"
BASE_URL = f"https://{RAPIDAPI_HOST}/flights/airports/icao"

# Parámetros de ejemplo
ORIGEN_ICAO_DEFAULT = "JFK"  # John F. Kennedy Intl (más datos disponibles)

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}


def get_real_time_flights(fecha: datetime.date, origen_icao=ORIGEN_ICAO_DEFAULT):
    """
    Solicita vuelos programados (salidas y llegadas) desde un aeropuerto específico en una fecha.
    Usa el endpoint FIDS: /flights/airports/icao/{code}/{fromLocal}/{toLocal}
    Divide el día en dos rangos de 12 horas para cumplir con la restricción de la API.
    Soporta respuesta con 'movement' (nuevo formato AeroDataBox).
    """
    try:
        fecha_str = fecha.strftime('%Y-%m-%d')
        rangos = [
            (f"{fecha_str}T00:00", f"{fecha_str}T12:00"),
            (f"{fecha_str}T12:00", f"{fecha_str}T23:59")
        ]
        vuelos = []
        for from_local, to_local in rangos:
            url = f"https://{RAPIDAPI_HOST}/flights/airports/icao/{origen_icao}/{from_local}/{to_local}"
            params = {"direction": "Both"}
            response = requests.get(url, headers=HEADERS, params=params)
            if response.status_code == 404:
                print(f"⚠️  No hay datos disponibles para {origen_icao} en {from_local} - {to_local} (404 Not Found)")
                continue
            if response.status_code != 200:
                print(f"❌ Error {response.status_code} AeroDataBox: {response.text}")
                continue
            try:
                data = response.json()
            except Exception as e:
                print(f"❌ Error al parsear JSON de AeroDataBox: {e}. Respuesta: {response.text}")
                continue
            # Nuevo formato: lista de vuelos en 'departures', 'arrivals' o directamente en la raíz
            vuelos_list = []
            if "departures" in data:
                vuelos_list.extend(data["departures"])
            if "arrivals" in data:
                vuelos_list.extend(data["arrivals"])
            # Si la respuesta es una lista directa (como en el ejemplo crudo)
            if isinstance(data, list):
                vuelos_list.extend(data)
            # Si la respuesta es un dict con 'flights' o similar
            if "flights" in data:
                vuelos_list.extend(data["flights"])
            print(f"✈️ Vuelos recibidos para {origen_icao} en {from_local}-{to_local}: {len(vuelos_list)}")
            vuelos.extend(vuelos_list)
        return vuelos

    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la solicitud a AeroDataBox: {e}")
        return []
