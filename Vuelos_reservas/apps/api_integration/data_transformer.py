# apps/api_integration/data_transformer.py

from datetime import datetime
from .constants import ESTADOS_VUELO_VALIDOS


def transform_real_flight_data(raw_flight):
    """
    Transforma un vuelo real proveniente de Aviationstack en una estructura lista para insertar.
    """
    try:
        airline_data = raw_flight.get('airline') or {}
        departure_data = raw_flight.get('departure') or {}
        arrival_data = raw_flight.get('arrival') or {}
        flight_data = raw_flight.get('flight') or {}
        aircraft_data = raw_flight.get('aircraft') or {}

        return {
            'numero_vuelo': flight_data.get('iata', 'N/A'),
            'aerolinea': {
                'nombre': airline_data.get('name'),
                'codigo_iata': airline_data.get('iata'),
            },
            'origen': {
                'codigo_iata': departure_data.get('iata'),
                'nombre': departure_data.get('airport'),
                'ciudad': departure_data.get('city'),
                'pais': departure_data.get('country'),
            },
            'destino': {
                'codigo_iata': arrival_data.get('iata'),
                'nombre': arrival_data.get('airport'),
                'ciudad': arrival_data.get('city'),
                'pais': arrival_data.get('country'),
            },
            'fecha_salida': departure_data.get('scheduled'),
            'fecha_llegada': arrival_data.get('scheduled'),
            'modelo_avion': aircraft_data.get('icao'),
            'estado': ESTADOS_VUELO_VALIDOS.get(raw_flight.get('flight_status'), 'Desconocido'),
            'es_simulado': False
        }

    except Exception as e:
        print(f"Error al transformar vuelo real: {e}")
        return None


def transform_simulated_flight_data(sim_flight):
    """
    Transforma un vuelo simulado (generado internamente) al formato esperado por el modelo Vuelo.
    """
    return {
        'numero_vuelo': sim_flight['numero_vuelo'],
        'aerolinea': sim_flight['aerolinea'],
        'origen': sim_flight['origen'],
        'destino': sim_flight['destino'],
        # Adaptar a los campos del modelo Vuelo:
        'fecha_salida_programada': sim_flight['fecha_salida'],
        'fecha_llegada_programada': sim_flight['fecha_llegada'],
        'modelo_avion': sim_flight['modelo_avion'],
        'flight_date': sim_flight['fecha_salida'][:10],
        'flight_status': 'Programado',
        'precio_base': 1000.00,
        'asientos_disponibles': 100,
        'duracion_minutos': 120,
        'api_flight_iata': sim_flight['numero_vuelo'],
        'api_flight_icao': '',
        'codeshare_info': '',
        'es_simulado': True,
        # Campos opcionales
        'fecha_salida_real': None,
        'fecha_llegada_real': None,
        'terminal_salida': '',
        'gate_salida': '',
        'terminal_llegada': '',
        'gate_llegada': '',
    }
