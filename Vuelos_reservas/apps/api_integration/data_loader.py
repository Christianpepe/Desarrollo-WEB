def get_or_create_aerolinea(data):

#  Funciones para guardar vuelos y entidades relacionadas en la base de datos
from apps.vuelos.models import Vuelo, Aerolinea, Aeropuerto, ModeloAvion
from django.db import transaction

# Aerolínea 
def get_or_create_aerolinea(data):
    """Obtiene o crea una aerolínea por código IATA."""
    return Aerolinea.objects.get_or_create(
        codigo_iata=data['codigo_iata'],
        defaults={'nombre': data['nombre']}
    )[0]


def get_or_create_aeropuerto(data):
    """Obtiene o crea un aeropuerto por código ICAO. Si existe y el IATA cambió, lo actualiza."""
    aeropuerto, creado = Aeropuerto.objects.get_or_create(
        codigo_icao=data.get('codigo_icao', ''),
        defaults={
            'codigo_iata': data.get('codigo_iata', ''),
            'nombre': data.get('nombre', ''),
            'ciudad': data.get('ciudad') or '',
            'pais': data.get('pais') or '',
            'latitud': data.get('latitud') if data.get('latitud') is not None else 0.0,
            'longitud': data.get('longitud') if data.get('longitud') is not None else 0.0,
            'timezone': data.get('timezone', ''),
            'activo': True
        }
    )
    # Si existe pero el IATA es diferente y no está vacío, actualiza el IATA
    if not creado and data.get('codigo_iata') and aeropuerto.codigo_iata != data.get('codigo_iata'):
        aeropuerto.codigo_iata = data.get('codigo_iata')
        aeropuerto.save()
    return aeropuerto


def get_or_create_modelo_avion(codigo):
    """Obtiene o crea un modelo de avión por código."""
    if not codigo:
        return None
    return ModeloAvion.objects.get_or_create(
        codigo=codigo,
        defaults={'nombre': codigo, 'capacidad_total': 100, 'filas_total': 25, 'asientos_por_fila': 4}
    )[0]


def guardar_vuelo(data):

@transaction.atomic
def guardar_vuelo(data):
    """
    Guarda o actualiza un vuelo (real o simulado) en la base de datos.
    Si ya existe (por número y fecha), lo actualiza.
    """
    try:
        aerolinea = get_or_create_aerolinea(data['aerolinea'])
        origen = get_or_create_aeropuerto(data['origen'])
        destino = get_or_create_aeropuerto(data['destino'])
        modelo = get_or_create_modelo_avion(data.get('modelo_avion'))

        vuelo, creado = Vuelo.objects.update_or_create(
            numero_vuelo=data['numero_vuelo'],
            flight_date=data['flight_date'],
            defaults={
                'aerolinea': aerolinea,
                'aeropuerto_origen': origen,
                'aeropuerto_destino': destino,
                'modelo_avion': modelo,
                'flight_status': data.get('flight_status', 'Programado'),
                'fecha_salida_programada': data['fecha_salida_programada'],
                'fecha_llegada_programada': data['fecha_llegada_programada'],
                'fecha_salida_real': data.get('fecha_salida_real'),
                'fecha_llegada_real': data.get('fecha_llegada_real'),
                'terminal_salida': data.get('terminal_salida', ''),
                'gate_salida': data.get('gate_salida', ''),
                'terminal_llegada': data.get('terminal_llegada', ''),
                'gate_llegada': data.get('gate_llegada', ''),
                'precio_base': data.get('precio_base', 1000.00),
                'asientos_disponibles': data.get('asientos_disponibles', 100),
                'duracion_minutos': data.get('duracion_minutos', 120),
                'api_flight_iata': data.get('api_flight_iata', ''),
                'api_flight_icao': data.get('api_flight_icao', ''),
                'codeshare_info': data.get('codeshare_info', ''),
                # 'es_simulado': data.get('es_simulado', False),
            }
        )
        return vuelo, creado
    except Exception:
        return None, False
