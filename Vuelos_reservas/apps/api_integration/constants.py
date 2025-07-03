
#  onstantes y parámetros globales.
import os
from decouple import config

# Configuración de la API AeroDataBox 
RAPIDAPI_KEY = config('RAPIDAPI_KEY')
RAPIDAPI_HOST = config('RAPIDAPI_HOST')
AERODATABOX_BASE_URL = 'https://aerodatabox.p.rapidapi.com'

# Parámetros de consulta y simulación
DIAS_A_CONSULTAR = 5  # Cuántos días hacia adelante consultar
NUM_SIMULATED_FLIGHTS_PER_DAY = 10  # Vuelos simulados por día
SIMULATED_DAYS = 5  # Días futuros a simular

#  Filtros opcionales
AEROLINEAS_FILTRADAS = []  
AEROPUERTOS_FILTRADOS = [] 

#Estados de vuelo válidos según la APi
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


DEFAULT_PAGE_SIZE = 100  # Límite por página de resultados en la API
SIMULATED_DAYS = 5  # Días futuros a simular

