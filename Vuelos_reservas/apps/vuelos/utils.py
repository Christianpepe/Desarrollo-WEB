from apps.vuelos.models import Asiento, Vuelo

def generar_asientos_para_vuelo(vuelo):
    """
    Genera asientos automáticamente para el vuelo según su modelo de avión.
    """
    modelo = vuelo.modelo_avion
    # Limitar a 14 filas y 4 columnas (A, B, C, D) = 56 asientos
    filas = 14
    columnas = 4
    letras_columnas = 'ABCD'
    asientos = []
    for fila in range(1, filas + 1):
        for col_idx in range(columnas):
            letra = letras_columnas[col_idx]
            numero_asiento = f"{fila}{letra}"
            asientos.append(Asiento(
                vuelo=vuelo,
                numero_asiento=numero_asiento,
                fila=fila,
                columna=letra,
                clase="Económica",
            ))
    Asiento.objects.bulk_create(asientos)
