# apps/api_integration/data_loader.py

from apps.vuelos.models import Vuelo, Aerolinea, Aeropuerto, ModeloAvion
from django.utils.dateparse import parse_datetime
from django.db import transaction


def get_or_create_aerolinea(data):
    return Aerolinea.objects.get_or_create(
        codigo_iata=data['codigo_iata'],
        defaults={'nombre': data['nombre']}
    )[0]


def get_or_create_aeropuerto(data):
    return Aeropuerto.objects.get_or_create(
        codigo_iata=data['codigo_iata'],
        defaults={
            'nombre': data.get('nombre', ''),
            'ciudad': data.get('ciudad') or '',
            'pais': data.get('pais') or '',
            'latitud': data.get('latitud') if data.get('latitud') is not None else 0.0,
            'longitud': data.get('longitud') if data.get('longitud') is not None else 0.0,
            'codigo_icao': data.get('codigo_icao', ''),
            'timezone': data.get('timezone', ''),
            'activo': True
        }
    )[0]


def get_or_create_modelo_avion(codigo):
    if not codigo:
        return None
    return ModeloAvion.objects.get_or_create(
        codigo=codigo,
        defaults={'nombre': codigo, 'capacidad_total': 100, 'filas_total': 25, 'asientos_por_fila': 4}
    )[0]


@transaction.atomic
def guardar_vuelo(data):
    """
    Guarda o actualiza un vuelo (real o simulado) en la base de datos.
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
                # 'es_simulado': data.get('es_simulado', False), # Si tienes este campo en el modelo
            }
        )

        return vuelo, creado
    except Exception as e:
        print(f"Error al guardar vuelo: {e}")
        return None, False
