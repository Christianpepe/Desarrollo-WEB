# Wrapper para integración: acepta solo strings y modelo, y construye el diccionario esperado
def estimar_precio_y_duracion_from_iata(origen_iata, destino_iata, modelo, clase='economica', fecha=None):
    vuelo = {
        'numero_vuelo': 'A',  # Default, no relevante para precio real
        'origen': {'codigo_iata': origen_iata},
        'destino': {'codigo_iata': destino_iata},
        'modelo_avion': modelo or 'GENERIC',
    }
    vuelo = estimar_precio_y_duracion(vuelo, clase=clase, fecha=fecha)
    return vuelo['precio_base'], vuelo['duracion_estimada_horas']
# Aquí irá la lógica de estimación de precios y duración de vuelos

import random
from datetime import datetime

letras_precio = {
    'A': 3000,
    'G': 3000,
    'R': 2800,
    'Y': 3200,
    'Z': 3100,
}

destinos_populares = {
    'CUN', 'CDG', 'LAX', 'NYC', 'FCO', 'TYO', 'LON',
    'BKK', 'ROM', 'DXB', 'PDC', 'TUL', 'PXM', 'MEX'
}

meses_temporada_alta = {12, 7, 4}


def estimar_precio_y_duracion(vuelo, clase='economica', fecha=None):
    """
    Estima el precio del vuelo y su duración basada en ese precio.
    Modifica el diccionario 'vuelo' agregando 'precio_base' y 'duracion_estimada_horas'.
    """
    # 1. Precio base por letra y aleatoriedad
    letra = vuelo.get('codigo_vuelo', vuelo.get('numero_vuelo', 'A'))[0].upper()
    base = letras_precio.get(letra, random.randint(2000, 2800))
    # Variabilidad extra: suma aleatoria entre -500 y +1500
    variacion = random.randint(-500, 1500)
    precio = base + variacion

    # 2. Aumento si destino/origen es turístico
    iata = None
    if 'destino' in vuelo and 'codigo_iata' in vuelo['destino']:
        iata = vuelo['destino']['codigo_iata']
    elif 'origen' in vuelo and 'codigo_iata' in vuelo['origen']:
        iata = vuelo['origen']['codigo_iata']

    if iata and iata.upper() in destinos_populares:
        precio += 2000

    # 3. Aumento por temporada alta
    mes = fecha.month if fecha else datetime.now().month
    if mes in meses_temporada_alta:
        precio += 1000

    # 4. Clase de boleto
    if clase.lower() == 'primera':
        precio *= 4

    # Redondear a múltiplos de 50
    precio = round(precio / 50) * 50
    vuelo['precio_base'] = precio

    # 5. Estimación de duración según precio
    if precio < 3000:
        duracion = round(random.uniform(0.5, 1.5), 2)
    elif precio <= 6000:
        duracion = round(random.uniform(1.5, 3.5), 2)
    else:
        duracion = round(random.uniform(4.0, 7.0), 2)

    vuelo['duracion_estimada_horas'] = duracion

    return vuelo
