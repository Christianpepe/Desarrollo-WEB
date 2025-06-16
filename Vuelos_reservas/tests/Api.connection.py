import requests

# Reemplaza con tu propia API Key
API_KEY = ''

# Endpoint base
url = 'http://api.aviationstack.com/v1/flights'

# Parámetros de prueba (puede filtrar por fecha, aerolínea, aeropuerto, etc.)
params = {
    'access_key': API_KEY,
    'limit': 1  # Solo pedimos un vuelo para probar
}

# Hacer la solicitud
response = requests.get(url, params=params)

# Revisar si la conexión fue exitosa
if response.status_code == 200:
    data = response.json()
    print("✅ Conexión exitosa. Ejemplo de datos:")
    print(data)
else:
    print("❌ Error en la conexión. Código:", response.status_code)
    print(response.text)
