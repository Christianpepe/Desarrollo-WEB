# apps/api_integration/constants.py

import os
from decouple import config

#  API config para AeroDataBox
RAPIDAPI_KEY = config('RAPIDAPI_KEY')
RAPIDAPI_HOST = config('RAPIDAPI_HOST')
AERODATABOX_BASE_URL = 'https://aerodatabox.p.rapidapi.com'

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
DEFAULT_PAGE_SIZE = 100  # Límite por página de resultados en la API (máximo permitido por Aviationstack)

# Simulación
NUM_SIMULATED_FLIGHTS_PER_DAY = 10
SIMULATED_DAYS = 5  # Días futuros a simular

