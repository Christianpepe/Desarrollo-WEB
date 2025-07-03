def get_real_time_flights(fecha: datetime.date, origen_icao=ORIGEN_ICAO_DEFAULT):

# api_client.py: Cliente para la API de AeroDataBox
import requests
from datetime import datetime
from decouple import config

# Configuración de la API
RAPIDAPI_KEY = config("RAPIDAPI_KEY") 
RAPIDAPI_HOST = "aerodatabox.p.rapidapi.com"
BASE_URL = f"https://{RAPIDAPI_HOST}/flights/airports/icao"


# Headers para autenticación
HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}

def get_real_time_flights(fecha: datetime.date, origen_icao=ORIGEN_ICAO_DEFAULT):
    """
    Solicita vuelos programados (salidas y llegadas) desde un aeropuerto específico en una fecha.
    """
    vuelos_list = []
    for direction in ["departures", "arrivals"]:
        url = f"https://{RAPIDAPI_HOST}/flights/airports/icao/{origen_icao}"
        params = {
            "direction": direction[:-1].capitalize(),  # 'Departure' o 'Arrival'
            "offsetMinutes": -120,
            "durationMinutes": 720
        }
        try:
            response = requests.get(url, headers=HEADERS, params=params)
            if response.status_code != 200:
                continue  # Si no hay datos o error, omitir
            data = response.json()
        except Exception:
            continue
        # Extrae los vuelos según la clave de la respuesta
        if direction in data:
            for vuelo in data[direction]:
                vuelo["_direction"] = direction
                vuelo["_consulted_icao"] = origen_icao
                vuelos_list.append(vuelo)
        elif isinstance(data, list):
            for vuelo in data:
                vuelo["_direction"] = direction
                vuelo["_consulted_icao"] = origen_icao
                vuelos_list.append(vuelo)
        elif "flights" in data:
            for vuelo in data["flights"]:
                vuelo["_direction"] = direction
                vuelo["_consulted_icao"] = origen_icao
                vuelos_list.append(vuelo)
    return vuelos_list
