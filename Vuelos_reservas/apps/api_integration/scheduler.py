
"""
scheduler.py
Maneja  la carga de vuelos y los simulados en el sistema y trasnforma los datos para la BDD.
"""

from datetime import datetime, timedelta
from apps.api_integration.api_client import get_real_time_flights
from apps.api_integration.data_transformer import transformar_vuelo_a_modelo
from apps.api_integration.data_simulator import generate_simulated_flights
from apps.api_integration.data_loader import guardar_vuelo

def ejecutar_carga_completa(dias_a_consultar=3, cargar_reales=True, cargar_simulados=True, icao_code=None):
    """
    Ejecuta la carga completa de vuelos reales (desde la API) y simulados.
    """
    vuelos_cargados = 0

    # Carga de vuelosdesde la API 
    if cargar_reales:
        hoy = datetime.now().date()
        for offset in range(1, dias_a_consultar + 1):
            fecha = hoy - timedelta(days=offset)
            # Consulta vuelos reales para la fecha y aeropuerto 
            vuelos_api = get_real_time_flights(fecha, origen_icao=icao_code) if icao_code else get_real_time_flights(fecha)
            for vuelo_api in vuelos_api:
                transformado = transformar_vuelo_a_modelo(vuelo_api, es_simulado=False)
                if transformado:
                    vuelo, creado = guardar_vuelo(transformado)
                    if creado:
                        vuelos_cargados += 1

    # Carga de vuelos simulados 
    if cargar_simulados:
        simulados = generate_simulated_flights()
        for vuelo_simulado in simulados:
            vuelo, creado = guardar_vuelo(vuelo_simulado)
            if creado:
                vuelos_cargados += 1

    # Fin 
    return vuelos_cargados
