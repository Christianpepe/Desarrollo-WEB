from datetime import datetime, timedelta
from apps.api_integration.api_client import get_real_time_flights
from apps.api_integration.data_transformer import transformar_vuelo_a_modelo
from apps.api_integration.data_simulator import generate_simulated_flights
from apps.api_integration.data_loader import guardar_vuelo


def ejecutar_carga_completa(dias_a_consultar=3, cargar_reales=True, cargar_simulados=True, icao_code=None):
    vuelos_cargados = 0

    if cargar_reales:
        print("🔍 Obteniendo vuelos reales desde la API...")

        hoy = datetime.now().date()
        # Consultar solo días pasados (no el día actual ni futuros)
        for offset in range(1, dias_a_consultar + 1):
            fecha = hoy - timedelta(days=offset)
            if icao_code:
                vuelos_api = get_real_time_flights(fecha, origen_icao=icao_code)
            else:
                vuelos_api = get_real_time_flights(fecha)

            for vuelo_api in vuelos_api:
                transformado = transformar_vuelo_a_modelo(vuelo_api, es_simulado=False)
                if transformado:
                    vuelo, creado = guardar_vuelo(transformado)
                    if creado:
                        vuelos_cargados += 1

    if cargar_simulados:
        print("🎲 Generando vuelos simulados...")
        simulados = generate_simulated_flights()
        for vuelo_simulado in simulados:
            vuelo, creado = guardar_vuelo(vuelo_simulado)
            if creado:
                vuelos_cargados += 1

    print(f"✅ Carga finalizada. Total de vuelos nuevos: {vuelos_cargados}")
