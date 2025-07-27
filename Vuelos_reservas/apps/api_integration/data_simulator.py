

#  Generador de vuelos simulados para pruebas 
import random
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from .constants import SIMULATED_DAYS, NUM_SIMULATED_FLIGHTS_PER_DAY
# Importar la función de estimación de precio y duración de la API nativa
from apps.api_nativa.utils import estimar_precio_y_duracion

#  Datos base de ejemplo para simulación
AEROLINEAS_SIMULADAS = [
    {'nombre': 'Aerolíneas Simuladas MX', 'codigo_iata': 'SM'},
    {'nombre': 'Virtual Airlines', 'codigo_iata': 'VA'}
]

AEROPUERTOS_SIMULADOS = [
    {'codigo_iata': 'MEX', 'nombre': 'Benito Juárez', 'ciudad': 'Ciudad de México', 'pais': 'México', 'latitud': 19.4361, 'longitud': -99.0719},
    {'codigo_iata': 'JFK', 'nombre': 'John F. Kennedy', 'ciudad': 'Nueva York', 'pais': 'Estados Unidos', 'latitud': 40.6413, 'longitud': -73.7781},
    {'codigo_iata': 'LAX', 'nombre': 'Los Angeles Intl', 'ciudad': 'Los Ángeles', 'pais': 'Estados Unidos', 'latitud': 33.9416, 'longitud': -118.4085},
    {'codigo_iata': 'MAD', 'nombre': 'Barajas', 'ciudad': 'Madrid', 'pais': 'España', 'latitud': 40.4983, 'longitud': -3.5676}
]

MODELOS_AVION_SIMULADOS = ['A320', 'B737', 'E190']

def generate_simulated_flights():
    """
    Genera una lista de vuelos simulados para poblar la base de datos en desarrollo o pruebas.
    Cada vuelo tiene datos coherentes y fechas distribuidas en varios días.
    """
    vuelos = []
    base_fecha = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    for dia in range(SIMULATED_DAYS):
        fecha_actual = base_fecha + timedelta(days=dia)
        for _ in range(NUM_SIMULATED_FLIGHTS_PER_DAY):
            aerolinea = random.choice(AEROLINEAS_SIMULADAS)
            origen, destino = random.sample(AEROPUERTOS_SIMULADOS, 2)
            modelo_avion = random.choice(MODELOS_AVION_SIMULADOS)
            hora_salida = fecha_actual + timedelta(minutes=random.randint(0, 600))
            duracion = timedelta(minutes=random.randint(90, 300))
            hora_llegada = hora_salida + duracion
            # Convertir a timezone-aware
            hora_salida = make_aware(hora_salida)
            hora_llegada = make_aware(hora_llegada)

            # Calcular precio realista usando la función de la API nativa
            precio_base, _ = estimar_precio_y_duracion(
                origen['codigo_iata'], destino['codigo_iata'], modelo_avion, hora_salida, hora_llegada
            )

            vuelos.append({
                'numero_vuelo': f"{aerolinea['codigo_iata']}{random.randint(100, 999)}",
                'aerolinea': aerolinea,
                'origen': origen,
                'destino': destino,
                'fecha_salida': hora_salida.isoformat(),
                'fecha_llegada': hora_llegada.isoformat(),
                'fecha_salida_programada': hora_salida.isoformat(),
                'fecha_llegada_programada': hora_llegada.isoformat(),
                'modelo_avion': modelo_avion,
                'flight_date': hora_salida.date().isoformat(),
                'precio_base': precio_base,
            })
    return vuelos
