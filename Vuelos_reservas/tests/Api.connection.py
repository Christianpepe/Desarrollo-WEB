import requests
from datetime import datetime
from decouple import config

# Configuración para AeroDataBox
RAPIDAPI_KEY = config("RAPIDAPI_KEY")
RAPIDAPI_HOST = "aerodatabox.p.rapidapi.com"

# Cambia aquí el aeropuerto y la fecha que quieras probar
ICAO = 'KLAX'  # Cambia por el ICAO deseado
fecha = datetime.now().strftime('%Y-%m-%d')

# Rango de 12 horas (puedes ajustar)
from_local = f"{fecha}T00:00"
to_local = f"{fecha}T12:00"

url = f"https://{RAPIDAPI_HOST}/flights/airports/icao/{ICAO}/{from_local}/{to_local}"

headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}
params = {"direction": "Both"}

response = requests.get(url, headers=headers, params=params)

print(f"URL consultada: {response.url}")
print(f"Código de estado: {response.status_code}")
print("Respuesta cruda de la API:")
print(response.text)
