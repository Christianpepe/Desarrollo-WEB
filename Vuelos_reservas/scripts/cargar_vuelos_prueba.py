from apps.api_integration.data_loader import guardar_vuelo
from datetime import datetime

# Ejemplo de datos para dos aeropuertos diferentes (diferente ICAO)

vuelos = [
    {
        'numero_vuelo': 'TEST001',
        'flight_date': '2025-07-03',
        'aerolinea': {'codigo_iata': 'AA', 'nombre': 'American Airlines'},
        'origen': {
            'codigo_icao': 'MMMX',
            'codigo_iata': 'MEX',
            'nombre': 'Aeropuerto CDMX',
            'ciudad': 'Ciudad de México',
            'pais': 'México',
            'latitud': 19.4361,
            'longitud': -99.0719,
            'timezone': 'America/Mexico_City',
        },
        'destino': {
            'codigo_icao': 'MMMY',
            'codigo_iata': 'MTY',
            'nombre': 'Aeropuerto Monterrey',
            'ciudad': 'Monterrey',
            'pais': 'México',
            'latitud': 25.7785,
            'longitud': -100.1071,
            'timezone': 'America/Monterrey',
        },
        'modelo_avion': 'A320',
        'flight_status': 'Programado',
        'fecha_salida_programada': datetime(2025, 7, 3, 15, 0),
        'fecha_llegada_programada': datetime(2025, 7, 3, 17, 0),
    },
    {
        'numero_vuelo': 'TEST002',
        'flight_date': '2025-07-03',
        'aerolinea': {'codigo_iata': 'AA', 'nombre': 'American Airlines'},
        'origen': {
            'codigo_icao': 'MMMY',
            'codigo_iata': 'MTY',
            'nombre': 'Aeropuerto Monterrey',
            'ciudad': 'Monterrey',
            'pais': 'México',
            'latitud': 25.7785,
            'longitud': -100.1071,
            'timezone': 'America/Monterrey',
        },
        'destino': {
            'codigo_icao': 'MMMX',
            'codigo_iata': 'MEX',
            'nombre': 'Aeropuerto CDMX',
            'ciudad': 'Ciudad de México',
            'pais': 'México',
            'latitud': 19.4361,
            'longitud': -99.0719,
            'timezone': 'America/Mexico_City',
        },
        'modelo_avion': 'A320',
        'flight_status': 'Programado',
        'fecha_salida_programada': datetime(2025, 7, 3, 18, 0),
        'fecha_llegada_programada': datetime(2025, 7, 3, 20, 0),
    },
]

for vuelo in vuelos:
    obj, creado = guardar_vuelo(vuelo)
    print(f"Vuelo {vuelo['numero_vuelo']} {'creado' if creado else 'actualizado'}.")
