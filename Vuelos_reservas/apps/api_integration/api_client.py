# apps/api_integration/api_client.py

import requests
from datetime import datetime, timedelta
from .constants import (
    AVIATIONSTACK_API_KEY,
    FLIGHTS_ENDPOINT,
    DIAS_A_CONSULTAR,
    DEFAULT_PAGE_SIZE,
    AEROLINEAS_FILTRADAS,
    AEROPUERTOS_FILTRADOS
)



def get_real_time_flights(limit=10):
    """
    Obtiene vuelos reales de la API Aviationstack. Si falla, retorna una lista vacía.
    """
    all_flights = []
    today = datetime.now()
    try:
        for i in range(DIAS_A_CONSULTAR):
            date_obj = today + timedelta(days=i)
            flights = fetch_flights_for_day(date_obj)
            all_flights.extend(flights)
            if len(all_flights) >= limit:
                break
        # Limitar al número solicitado
        return all_flights[:limit]
    except Exception as e:
        print(f"Error general al obtener vuelos reales: {e}")
        return []

def get_real_time_flights(limit=10):
    """
    Llama a la API de Aviationstack para obtener vuelos en tiempo real.
    """
    params = {
        'access_key': AVIATIONSTACK_API_KEY,
        'limit': limit
    }

    if AEROLINEAS_FILTRADAS:
        params['airline_iata'] = ','.join(AEROLINEAS_FILTRADAS)

    if AEROPUERTOS_FILTRADOS:
        params['dep_iata'] = ','.join(AEROPUERTOS_FILTRADOS)

    try:
        response = requests.get(FLIGHTS_ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('data', [])

    except requests.RequestException as e:
        print(f"Error al llamar a la API de Aviationstack: {e}")
        return []
