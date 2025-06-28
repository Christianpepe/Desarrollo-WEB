from datetime import datetime
from pytz import timezone


def trunc20(val):
    return str(val)[:20] if val else ''


def transformar_vuelo_a_modelo(vuelo_api, es_simulado=False):
    """
    Transforma un vuelo crudo de la API AeroDataBox o simulado a un formato compatible con guardar_vuelo.
    Soporta formato con 'movement' (nuevo formato AeroDataBox).
    """
    try:
        flight_info = vuelo_api

        # Si es simulado, adaptar los campos mínimos
        if es_simulado:
            numero_vuelo = trunc20(flight_info.get("numero_vuelo", "N/A"))
            return {
                "numero_vuelo": numero_vuelo,
                "flight_date": flight_info.get("flight_date"),
                "aerolinea": flight_info.get("aerolinea", {"nombre": "Desconocida", "codigo_iata": "ZZZ"}),
                "origen": flight_info.get("origen", {"codigo_iata": "ZZZ"}),
                "destino": flight_info.get("destino", {"codigo_iata": "ZZZ"}),
                "modelo_avion": trunc20(flight_info.get("modelo_avion", "GENERIC")),
                "estado": "Programado",
                "fecha_salida_programada": flight_info.get("fecha_salida"),
                "fecha_llegada_programada": flight_info.get("fecha_llegada"),
                "precio_base": 1000.00,
                "asientos_disponibles": 100,
                "duracion_minutos": 120,
                "api_flight_iata": trunc20(numero_vuelo),
                "api_flight_icao": "",
                "codeshare_info": "",
                "es_simulado": True,
                "fecha_salida_real": None,
                "fecha_llegada_real": None,
                "terminal_salida": "",
                "gate_salida": "",
                "terminal_llegada": "",
                "gate_llegada": "",
            }

        # Soporte para formato 'movement' (nuevo AeroDataBox)
        movement = flight_info.get("movement")
        if movement:
            aeropuerto = movement.get("airport", {})
            scheduled_time = movement.get("scheduledTime", {})
            revised_time = movement.get("revisedTime", {})
            runway_time = movement.get("runwayTime", {})
            flight_date = None
            if scheduled_time.get("local"):
                flight_date = parse_datetime_safe(scheduled_time.get("local"))
            elif revised_time.get("local"):
                flight_date = parse_datetime_safe(revised_time.get("local"))
            elif runway_time.get("local"):
                flight_date = parse_datetime_safe(runway_time.get("local"))
            if not flight_date:
                print(f"Vuelo omitido por falta de fecha programada: {flight_info.get('number', 'N/A')}")
                print(f"Contenido crudo del vuelo omitido: {flight_info}")
                return None
            modelo_avion = trunc20(flight_info.get("aircraft", {}).get("model", "GENERIC"))
            numero_vuelo = trunc20(flight_info.get("number", "N/A"))
            api_flight_iata = trunc20(flight_info.get("icaoNumber", ""))
            api_flight_icao = trunc20(flight_info.get("iataNumber", ""))
            # Asegurar que fecha_llegada_programada nunca sea nulo
            llegada_programada = parse_datetime_safe(revised_time.get("local")) or parse_datetime_safe(scheduled_time.get("local"))
            return {
                "numero_vuelo": numero_vuelo,
                "flight_date": flight_date.date(),
                "aerolinea": {
                    "nombre": trunc20(flight_info.get("airline", {}).get("name", "Desconocida")),
                    "codigo_iata": trunc20(flight_info.get("airline", {}).get("iata", "ZZZ")),
                },
                "origen": {
                    "codigo_iata": trunc20(aeropuerto.get("icao", "ZZZ")),
                    "nombre": trunc20(aeropuerto.get("name", "")),
                    "ciudad": "",
                    "pais": "",
                    "timezone": trunc20(aeropuerto.get("timeZone", "")),
                },
                "destino": {
                    "codigo_iata": "",
                    "nombre": "",
                    "ciudad": "",
                    "pais": "",
                    "timezone": "",
                },
                "modelo_avion": modelo_avion,
                "estado": trunc20(flight_info.get("status", "Programado")),
                "fecha_salida_programada": parse_datetime_safe(scheduled_time.get("local")),
                "fecha_llegada_programada": llegada_programada,
                "fecha_salida_real": parse_datetime_safe(runway_time.get("local")),
                "fecha_llegada_real": None,
                "terminal_salida": trunc20(movement.get("terminal", "")),
                "gate_salida": "",
                "terminal_llegada": "",
                "gate_llegada": "",
                "precio_base": 1000.00,
                "asientos_disponibles": 100,
                "duracion_minutos": 120,
                "api_flight_iata": api_flight_iata,
                "api_flight_icao": api_flight_icao,
                "codeshare_info": "",
                "es_simulado": es_simulado,
            }

        # Permitir guardar todos los vuelos, aunque no tengan departure ni arrival
        departure = flight_info.get("departure", {})
        arrival = flight_info.get("arrival", {})
        salida_programada = parse_datetime_safe(departure.get("scheduledTime", {}).get("local")) if departure else None
        llegada_programada = parse_datetime_safe(arrival.get("scheduledTime", {}).get("local")) if arrival else None
        salida_real = parse_datetime_safe(departure.get("actualTime", {}).get("local")) if departure else None
        llegada_real = parse_datetime_safe(arrival.get("actualTime", {}).get("local")) if arrival else None

        # Si no hay ninguna fecha programada, imprimir el vuelo crudo para depuración
        if not (salida_programada or llegada_programada):
            print(f"Vuelo omitido por falta de fecha programada: {flight_info.get('number', 'N/A')}")
            print(f"Contenido crudo del vuelo omitido: {flight_info}")
            return None

        modelo_avion = None
        if "aircraft" in flight_info and flight_info["aircraft"]:
            modelo_avion = flight_info["aircraft"].get("model") or "GENERIC"
        else:
            modelo_avion = "GENERIC"

        numero_vuelo = str(flight_info.get("number", "N/A"))[:20]
        api_flight_iata = str(flight_info.get("icaoNumber", ""))[:20]
        api_flight_icao = str(flight_info.get("iataNumber", ""))[:20]

        # Calcular duración si es posible
        duracion_minutos = 120
        if salida_programada and llegada_programada:
            duracion = (llegada_programada - salida_programada).total_seconds() / 60
            if duracion > 0:
                duracion_minutos = int(duracion)

        return {
            "numero_vuelo": numero_vuelo,
            "flight_date": (salida_programada or llegada_programada).date() if (salida_programada or llegada_programada) else None,
            "aerolinea": {
                "nombre": flight_info.get("airline", {}).get("name", "Desconocida"),
                "codigo_iata": flight_info.get("airline", {}).get("iata", "ZZZ"),
            },
            "origen": {
                "codigo_iata": departure.get("airport", {}).get("icao", "ZZZ") if departure else "ZZZ",
                "nombre": departure.get("airport", {}).get("name", "") if departure else "",
                "ciudad": departure.get("airport", {}).get("municipalityName", "") if departure else "",
                "pais": departure.get("airport", {}).get("countryCode", "") if departure else "",
                "timezone": departure.get("airport", {}).get("timeZone", "") if departure else "",
            },
            "destino": {
                "codigo_iata": arrival.get("airport", {}).get("icao", "ZZZ") if arrival else "ZZZ",
                "nombre": arrival.get("airport", {}).get("name", "") if arrival else "",
                "ciudad": arrival.get("airport", {}).get("municipalityName", "") if arrival else "",
                "pais": arrival.get("airport", {}).get("countryCode", "") if arrival else "",
                "timezone": arrival.get("airport", {}).get("timeZone", "") if arrival else "",
            },
            "modelo_avion": modelo_avion,
            "estado": flight_info.get("status", "Programado"),
            "fecha_salida_programada": salida_programada,
            "fecha_llegada_programada": llegada_programada,
            "fecha_salida_real": salida_real,
            "fecha_llegada_real": llegada_real,
            "terminal_salida": departure.get("terminal", "") if departure else "",
            "gate_salida": departure.get("gate", "") if departure else "",
            "terminal_llegada": arrival.get("terminal", "") if arrival else "",
            "gate_llegada": arrival.get("gate", "") if arrival else "",
            "precio_base": 1000.00,  # Puedes ajustar si tienes lógica dinámica
            "asientos_disponibles": 100,
            "duracion_minutos": duracion_minutos,
            "api_flight_iata": api_flight_iata,
            "api_flight_icao": api_flight_icao,
            "codeshare_info": "",
            "es_simulado": es_simulado,
        }

    except Exception as e:
        print(f" Error al transformar vuelo: {e}")
        return None


def parse_datetime_safe(dt_string):
    """
    Parsea un string de fecha en formato ISO 8601 y devuelve un objeto datetime con zona horaria local.
    """
    try:
        if dt_string:
            dt = datetime.fromisoformat(dt_string)
            if dt.tzinfo is None:
                # Si no trae tz, asumimos UTC
                dt = dt.replace(tzinfo=timezone("UTC"))
            return dt
    except Exception:
        pass
    return None
