# apps/api_integration/scheduler.py

from .api_client import get_real_time_flights
from .data_simulator import generate_simulated_flights
from .data_transformer import transform_real_flight_data, transform_simulated_flight_data
from .data_loader import guardar_vuelo


def ejecutar_carga_completa(cargar_reales=True, cargar_simulados=True):
    total_guardados = 0

    if cargar_reales:
        print("🔍 Obteniendo vuelos reales desde la API...")
        vuelos_reales = get_real_time_flights(limit=10)
        print(f"Respuesta cruda de la API (primeros 3): {vuelos_reales[:3]}")
        for vuelo_raw in vuelos_reales:
            if vuelo_raw is None or not isinstance(vuelo_raw, dict):
                print(f"Elemento inválido ignorado: {vuelo_raw}")
                continue  # Ignorar elementos None o inválidos
            vuelo_transformado = transform_real_flight_data(vuelo_raw)
            # Validar campos obligatorios antes de guardar
            if not vuelo_transformado:
                continue
            if not vuelo_transformado.get('fecha_salida') or not vuelo_transformado.get('aerolinea', {}).get('nombre') or not vuelo_transformado.get('origen', {}).get('nombre') or not vuelo_transformado.get('destino', {}).get('nombre'):
                print(f"Vuelo real ignorado por campos obligatorios faltantes: {vuelo_transformado}")
                continue
            if not vuelo_transformado.get('modelo_avion'):
                print(f"Vuelo real ignorado por modelo de avión faltante: {vuelo_transformado}")
                continue
            # Mapear campos para el modelo
            vuelo_transformado['fecha_salida_programada'] = vuelo_transformado.pop('fecha_salida', None)
            vuelo_transformado['fecha_llegada_programada'] = vuelo_transformado.pop('fecha_llegada', None)
            vuelo_transformado['flight_date'] = vuelo_raw.get('flight_date') or ''
            vuelo, creado = guardar_vuelo(vuelo_transformado)
            if creado:
                total_guardados += 1

    if cargar_simulados:
        print("🎲 Generando vuelos simulados...")
        vuelos_simulados = generate_simulated_flights()

        for vuelo_sim in vuelos_simulados:
            vuelo_transformado = transform_simulated_flight_data(vuelo_sim)
            if vuelo_transformado:
                vuelo, creado = guardar_vuelo(vuelo_transformado)
                if creado:
                    total_guardados += 1

    print(f"✅ Carga finalizada. Total de vuelos nuevos: {total_guardados}")
