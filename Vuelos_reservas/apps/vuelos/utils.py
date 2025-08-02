from Vuelos_reservas.apps.vuelos.models import Asiento, Vuelo
#CORONA GARCIA CHRISTIAN JAVIER
def generar_asientos_para_vuelo(vuelo):
    """
    Genera asientos automáticamente para el vuelo según su modelo de avión.
    Si el modelo tiene primera clase, genera ambos bloques de asientos.
    """
    modelo = vuelo.modelo_avion
    filas = 14
    columnas = 4
    letras_economica = 'ABCD'
    letras_primera = 'EFGH'
    asientos = []
    # Económica
    for fila in range(1, filas + 1):
        for col_idx in range(columnas):
            letra = letras_economica[col_idx]
            numero_asiento = f"{fila}{letra}"
            asientos.append(Asiento(
                vuelo=vuelo,
                numero_asiento=numero_asiento,
                fila=fila,
                columna=letra,
                clase="Económica",
            ))
    # Primera clase 
    if getattr(modelo, 'tiene_primera_clase', False):
        for fila in range(1, filas + 1):
            for col_idx in range(columnas):
                letra = letras_primera[col_idx]
                numero_asiento = f"{fila}{letra}"
                asientos.append(Asiento(
                    vuelo=vuelo,
                    numero_asiento=numero_asiento,
                    fila=fila,
                    columna=letra,
                    clase="Primera",
                ))
    Asiento.objects.bulk_create(asientos)
