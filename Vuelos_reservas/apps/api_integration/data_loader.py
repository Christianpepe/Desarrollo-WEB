#  Funciones para guardar vuelos y entidades relacionadas en la base de datos
#CORONA GARCIA CHRISTIAN JAVIER
from Vuelos_reservas.apps.vuelos.models import Vuelo, Aerolinea, Aeropuerto, ModeloAvion
from Vuelos_reservas.apps.vuelos.utils import generar_asientos_para_vuelo
from django.db import transaction
# Importar la función de estimación de precio y duración de la API nativa
from apps.api_nativa.utils import estimar_precio_y_duracion

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
    # Si existe pero el IATA es diferente 
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
        defaults={
            'nombre': codigo,
            'capacidad_total': 112,  # 14 filas x 4 columnas x 2 clases
            'filas_total': 14,
            'asientos_por_fila': 4,
            'tiene_primera_clase': True,
        }
    )[0]



# Utilidad para calcular el precio de primera clase
def calcular_precio_primera_clase(precio_base, factor=2.5):
    """Calcula el precio de primera clase a partir del precio base y un factor."""
    if precio_base is None:
        return None
    from decimal import Decimal, ROUND_HALF_UP
    if not isinstance(precio_base, float):
        factor_decimal = Decimal(str(factor))
        resultado = precio_base * factor_decimal
        return float(resultado.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    else:
        return round(precio_base * factor, 2)

@transaction.atomic
def guardar_vuelo(data):
    """
    Guarda o actualiza un vuelo (real o simulado) en la base de datos.
    Si ya existe (por número y fecha), lo actualiza.
    """
    try:
        aerolinea = get_or_create_aerolinea(data['aerolinea'])
        def ensure_dict(val):
            if isinstance(val, dict):
                return val
            elif isinstance(val, str):
                return {'codigo_iata': val}
            return {'codigo_iata': 'ZZZ'}
        origen_dict = ensure_dict(data.get('origen'))
        destino_dict = ensure_dict(data.get('destino'))
        origen = get_or_create_aeropuerto(origen_dict)
        destino = get_or_create_aeropuerto(destino_dict)
        modelo = get_or_create_modelo_avion(data.get('modelo_avion'))

        # Calcular precio realista SOLO con los datos que da la API
        aeropuerto_origen = origen_dict.get('codigo_iata', 'ZZZ')
        aeropuerto_destino = destino_dict.get('codigo_iata', 'ZZZ')
        # Si solo tienes uno, pon el otro como 'ZZZ' (default)
        if aeropuerto_origen == 'ZZZ' and aeropuerto_destino != 'ZZZ':
            aeropuerto_origen = 'ZZZ'
        if aeropuerto_destino == 'ZZZ' and aeropuerto_origen != 'ZZZ':
            aeropuerto_destino = 'ZZZ'
        # Simular fechas solo para cumplir con la base, pero no usarlas en el cálculo
        from apps.api_nativa.utils import estimar_precio_y_duracion_from_iata
        try:
            precio_base, _ = estimar_precio_y_duracion_from_iata(
                aeropuerto_origen,
                aeropuerto_destino,
                data.get('modelo_avion')
            )
        except Exception as e:
            print(f"Error calculando precio_base: {e}")
            precio_base = None
        if precio_base is None:
            faltantes = []
            if not aeropuerto_origen or aeropuerto_origen == 'ZZZ':
                faltantes.append('origen')
            if not aeropuerto_destino or aeropuerto_destino == 'ZZZ':
                faltantes.append('destino')
            if not modelo:
                faltantes.append('modelo_avion')
            print(f"[LOG] Vuelo {data.get('numero_vuelo')} guardado SIN precio_base. Faltó: {', '.join(faltantes) if faltantes else 'datos insuficientes'}")

        # Calcular asientos disponibles dinámicamente
        asientos_disponibles = 0
        if modelo:
            asientos_economicos = getattr(modelo, 'filas_total', 0) * getattr(modelo, 'asientos_por_fila', 0)
            asientos_primera = asientos_economicos if getattr(modelo, 'tiene_primera_clase', False) else 0
            asientos_disponibles = asientos_economicos + asientos_primera
        else:
            asientos_disponibles = 100

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
                'precio_base': precio_base,
                'asientos_disponibles': asientos_disponibles,
                'duracion_minutos': data.get('duracion_minutos', 120),
                'api_flight_iata': data.get('api_flight_iata', ''),
                'api_flight_icao': data.get('api_flight_icao', ''),
                'codeshare_info': data.get('codeshare_info', ''),
                # 'es_simulado': data.get('es_simulado', False),
            }
        )
        if creado:
            generar_asientos_para_vuelo(vuelo)
        # Ejemplo de uso para mostrar ambos precios en la vista/template:
        # precio_primera_clase = calcular_precio_primera_clase(vuelo.precio_base)
        # precio_economico = vuelo.precio_base
        return vuelo, creado
    except Exception as e:
        print(f"[ERROR guardar_vuelo] Vuelo {data.get('numero_vuelo')} no guardado. Motivo: {e}")
        return None, False
