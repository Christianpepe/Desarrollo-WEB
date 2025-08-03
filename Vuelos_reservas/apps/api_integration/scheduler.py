
"""
scheduler.py
Maneja  la carga de vuelos y los simulados en el sistema y trasnforma los datos para la BDD.
"""
#CORONA GARCIA CHRISTIAN JAVIER
from datetime import datetime, timedelta
from Vuelos_reservas.apps.api_integration.api_client import get_real_time_flights
from Vuelos_reservas.apps.api_integration.data_transformer import transformar_vuelo_a_modelo
from Vuelos_reservas.apps.api_integration.data_simulator import generate_simulated_flights
from Vuelos_reservas.apps.api_integration.data_loader import guardar_vuelo

def ejecutar_carga_completa(dias_a_consultar=3, cargar_reales=True, cargar_simulados=True, icao_code=None):
    """
    Ejecuta la carga completa de vuelos reales (desde la API) y simulados.
    """
    vuelos_cargados = 0
    vuelos_api_total = 0
    vuelos_transformados = 0
    vuelos_guardados = 0
    vuelos_fallidos = 0

    # Carga de vuelos desde la API
    if cargar_reales:
        hoy = datetime.now().date()
        for offset in range(1, dias_a_consultar + 1):
            fecha = hoy - timedelta(days=offset)
            print(f"[LOG] Consultando vuelos reales para fecha: {fecha} y aeropuerto: {icao_code}")
            vuelos_api = get_real_time_flights(fecha, origen_icao=icao_code) if icao_code else get_real_time_flights(fecha)
            print(f"[LOG] Vuelos obtenidos de la API: {len(vuelos_api)}")
            vuelos_api_total += len(vuelos_api)
            for vuelo_api in vuelos_api:
                transformado = transformar_vuelo_a_modelo(vuelo_api, es_simulado=False)
                if transformado:
                    vuelos_transformados += 1
                    vuelo, creado = guardar_vuelo(transformado)
                    if creado:
                        vuelos_guardados += 1
                    else:
                        vuelos_fallidos += 1
                else:
                    vuelos_fallidos += 1
        print(f"[LOG] Resumen carga vuelos reales: Total API={vuelos_api_total}, Transformados={vuelos_transformados}, Guardados={vuelos_guardados}, Fallidos={vuelos_fallidos}")

    # Carga de vuelos simulados
    if cargar_simulados:
        simulados = generate_simulated_flights()
        print(f"[LOG] Vuelos simulados generados: {len(simulados)}")
        for vuelo_simulado in simulados:
            vuelo, creado = guardar_vuelo(vuelo_simulado)
            if creado:
                vuelos_guardados += 1
            else:
                vuelos_fallidos += 1
        print(f"[LOG] Resumen carga vuelos simulados: Generados={len(simulados)}, Guardados={vuelos_guardados}, Fallidos={vuelos_fallidos}")

    # Fin 
    return vuelos_cargados
