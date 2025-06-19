# apps/api_integration/constants.py

import os
from decouple import config

#  API config
AVIATIONSTACK_API_KEY = config('AVIATIONSTACK_API_KEY')
API_BASE_URL = 'http://api.aviationstack.com/v1'
FLIGHTS_ENDPOINT = f'{API_BASE_URL}/flights'

#  Parámetros de consulta
DIAS_A_CONSULTAR = 5  # Cuántos días hacia adelante consultar

#  Parámetros opcionales para limitar resultados
AEROLINEAS_FILTRADAS = []  # Ej: ['AM', 'AA'] si se quiere filtrar por aerolínea IATA
AEROPUERTOS_FILTRADOS = []  # Ej: ['MEX', 'JFK']

#  Estados de vuelo válidos según la API
ESTADOS_VUELO_VALIDOS = {
    'scheduled': 'Programado',
    'active': 'En vuelo',
    'landed': 'Aterrizado',
    'cancelled': 'Cancelado',
    'incident': 'Incidente',
    'diverted': 'Desviado'
}

#  Clases de asiento
CLASES_ASIENTO = ['economy', 'business', 'first']

#  Otros valores fijos o auxiliares que podrías necesitar
DEFAULT_PAGE_SIZE = 100  # Límite por página de resultados en la API

# Simulación
NUM_SIMULATED_FLIGHTS_PER_DAY = 10
SIMULATED_DAYS = 5  # Días futuros a simular

