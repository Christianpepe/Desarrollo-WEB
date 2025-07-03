def trunc20(val):
    return str(val)[:20] if val else ''
def transformar_vuelo_a_modelo(vuelo_api, es_simulado=False):
def parse_datetime_safe(dt_string):

# data_transformer.py: Transforma los datos crudos de la API a formato de modelo Django
from datetime import datetime
from pytz import timezone

def trunc20(val):
    """Trunca un valor a 20 caracteres para campos de longitud limitada."""
    return str(val)[:20] if val else ''

def transformar_vuelo_a_modelo(vuelo_api, es_simulado=False):
    """
    Transforma un vuelo crudo de la API AeroDataBox o simulado a un formato compatible con guardar_vuelo.
    Soporta formato con 'movement' (nuevo formato AeroDataBox) y el formato con 'departure'/'arrival'.
    """
    try:
        flight_info = vuelo_api

        #  Vuelos simulados 
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

        #  Formato nuevo AeroDataBox: departure/arrival 
        departure = flight_info.get("departure")
        arrival = flight_info.get("arrival")
        if (isinstance(departure, dict) and departure) or (isinstance(arrival, dict) and arrival):
            salida_programada = parse_datetime_safe(departure.get("scheduledTime", {}).get("local")) if departure else None
            llegada_programada = parse_datetime_safe(arrival.get("scheduledTime", {}).get("local")) if arrival else None
            salida_real = parse_datetime_safe(departure.get("actualTime", {}).get("local")) if departure else None
            llegada_real = parse_datetime_safe(arrival.get("actualTime", {}).get("local")) if arrival else None
            # Si falta la llegada, igualar a la salida (para cumplir NOT NULL)
            if not llegada_programada and salida_programada:
                llegada_programada = salida_programada
            if not salida_programada and llegada_programada:
                salida_programada = llegada_programada
            if not (salida_programada and llegada_programada):
                return None
            modelo_avion = trunc20(flight_info.get("aircraft", {}).get("model", "GENERIC"))
            numero_vuelo = trunc20(flight_info.get("number", "N/A"))
            api_flight_iata = trunc20(flight_info.get("icaoNumber", ""))
            api_flight_icao = trunc20(flight_info.get("iataNumber", ""))
            return {
                "numero_vuelo": numero_vuelo,
                "flight_date": (salida_programada or llegada_programada).date() if (salida_programada or llegada_programada) else None,
                "aerolinea": {
                    "nombre": trunc20(flight_info.get("airline", {}).get("name", "Desconocida")),
                    "codigo_iata": trunc20(flight_info.get("airline", {}).get("iata", "ZZZ")),
                },
                "origen": {
                    "codigo_icao": departure.get("airport", {}).get("icao", "ZZZ") if departure else "ZZZ",
                    "codigo_iata": departure.get("airport", {}).get("iata", "ZZZ") if departure else "ZZZ",
                    "nombre": departure.get("airport", {}).get("name", "") if departure else "",
                    "ciudad": departure.get("airport", {}).get("municipalityName", "") if departure else "",
                    "pais": departure.get("airport", {}).get("countryCode", "") if departure else "",
                    "timezone": departure.get("airport", {}).get("timeZone", "") if departure else "",
                },
                "destino": {
                    "codigo_icao": arrival.get("airport", {}).get("icao", "ZZZ") if arrival else "ZZZ",
                    "codigo_iata": arrival.get("airport", {}).get("iata", "ZZZ") if arrival else "ZZZ",
                    "nombre": arrival.get("airport", {}).get("name", "") if arrival else "",
                    "ciudad": arrival.get("airport", {}).get("municipalityName", "") if arrival else "",
                    "pais": arrival.get("airport", {}).get("countryCode", "") if arrival else "",
                    "timezone": arrival.get("airport", {}).get("timeZone", "") if arrival else "",
                },
                "modelo_avion": modelo_avion,
                "estado": trunc20(flight_info.get("status", "Programado")),
                "fecha_salida_programada": salida_programada,
                "fecha_llegada_programada": llegada_programada,
                "fecha_salida_real": salida_real,
                "fecha_llegada_real": llegada_real,
                "terminal_salida": departure.get("terminal", "") if departure else "",
                "gate_salida": departure.get("gate", "") if departure else "",
                "terminal_llegada": arrival.get("terminal", "") if arrival else "",
                "gate_llegada": arrival.get("gate", "") if arrival else "",
                "precio_base": 1000.00,
                "asientos_disponibles": 100,
                "duracion_minutos": 120,
                "api_flight_iata": api_flight_iata,
                "api_flight_icao": api_flight_icao,
                "codeshare_info": "",
                "es_simulado": es_simulado,
            }

        #Formato antiguo: movement 
        movement = flight_info.get("movement")
        if isinstance(movement, dict) and movement:
            direction = flight_info.get("_direction", "departures")
            salida_programada = parse_datetime_safe(movement.get("scheduledTime", {}).get("local"))
            salida_real = parse_datetime_safe(movement.get("actualTime", {}).get("local"))
            llegada_programada = salida_programada
            llegada_real = salida_real
            modelo_avion = trunc20(flight_info.get("aircraft", {}).get("model", "GENERIC"))
            numero_vuelo = trunc20(flight_info.get("number", "N/A"))
            api_flight_iata = trunc20(flight_info.get("icaoNumber", ""))
            api_flight_icao = trunc20(flight_info.get("iataNumber", ""))
            airline = flight_info.get("airline", {})
            airport = movement.get("airport", {})
            if direction == "departures":
                # ORIGEN es el aeropuerto consultado, DESTINO es movement.airport
                origen = {
                    "codigo_icao": flight_info.get("_consulted_icao", "ZZZ"),
                    "codigo_iata": "",
                    "nombre": "",
                    "ciudad": "",
                    "pais": "",
                    "timezone": "",
                }
                destino = {
                    "codigo_icao": airport.get("icao", "ZZZ"),
                    "codigo_iata": airport.get("iata", "ZZZ"),
                    "nombre": airport.get("name", ""),
                    "ciudad": "",
                    "pais": "",
                    "timezone": airport.get("timeZone", ""),
                }
            else:
                # ARRIVALS: ORIGEN es movement.airport, DESTINO es el aeropuerto consultado
                origen = {
                    "codigo_icao": airport.get("icao", "ZZZ"),
                    "codigo_iata": airport.get("iata", "ZZZ"),
                    "nombre": airport.get("name", ""),
                    "ciudad": "",
                    "pais": "",
                    "timezone": airport.get("timeZone", ""),
                }
                destino = {
                    "codigo_icao": flight_info.get("_consulted_icao", "ZZZ"),
                    "codigo_iata": "",
                    "nombre": "",
                    "ciudad": "",
                    "pais": "",
                    "timezone": "",
                }
            if not llegada_programada and salida_programada:
                llegada_programada = salida_programada
            if not salida_programada and llegada_programada:
                salida_programada = llegada_programada
            if not (salida_programada and llegada_programada):
                return None
            return {
                "numero_vuelo": numero_vuelo,
                "flight_date": salida_programada.date() if salida_programada else None,
                "aerolinea": {
                    "nombre": trunc20(airline.get("name", "Desconocida")),
                    "codigo_iata": trunc20(airline.get("iata", "ZZZ")),
                },
                "origen": origen,
                "destino": destino,
                "modelo_avion": modelo_avion,
                "estado": trunc20(flight_info.get("status", "Programado")),
                "fecha_salida_programada": salida_programada,
                "fecha_llegada_programada": llegada_programada,
                "fecha_salida_real": salida_real,
                "fecha_llegada_real": llegada_real,
                "terminal_salida": movement.get("terminal", ""),
                "gate_salida": movement.get("gate", ""),
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

        # si no es ninguno de los formatos esperados
        return None

    except Exception:
        return None

def parse_datetime_safe(dt_string):
    """Parsea un string de fecha en formato ISO 8601 y devuelve un objeto datetime con zona horaria local."""
    try:
        if dt_string:
            dt = datetime.fromisoformat(dt_string)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone("UTC"))
            return dt
    except Exception:
        pass
    return None
