
# models.py: Modelos principales del sistema de vuelos
from django.db import models

# --- Aeropuerto ---
class Aeropuerto(models.Model):
    codigo_iata = models.CharField(max_length=10, blank=True, null=True)  # Código IATA (opcional)
    codigo_icao = models.CharField(max_length=10, unique=True)            # Código ICAO (único)
    nombre = models.CharField(max_length=100)                            # Nombre del aeropuerto
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    timezone = models.CharField(max_length=50)
    latitud = models.DecimalField(max_digits=10, decimal_places=6)
    longitud = models.DecimalField(max_digits=10, decimal_places=6)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

# --- Aerolínea ---
class Aerolinea(models.Model):
    codigo_iata = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

# --- Modelo de avión ---
class ModeloAvion(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    capacidad_total = models.IntegerField()
    filas_total = models.IntegerField()
    asientos_por_fila = models.IntegerField()
    tiene_primera_clase = models.BooleanField(default=False)
    tiene_clase_ejecutiva = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# --- Vuelo ---
class Vuelo(models.Model):
    numero_vuelo = models.CharField(max_length=20)
    aerolinea = models.ForeignKey(Aerolinea, on_delete=models.CASCADE)
    aeropuerto_origen = models.ForeignKey(Aeropuerto, on_delete=models.CASCADE, related_name='salidas')
    aeropuerto_destino = models.ForeignKey(Aeropuerto, on_delete=models.CASCADE, related_name='llegadas')
    modelo_avion = models.ForeignKey(ModeloAvion, on_delete=models.CASCADE)
    flight_date = models.DateField()
    flight_status = models.CharField(max_length=50)
    fecha_salida_programada = models.DateTimeField()
    fecha_llegada_programada = models.DateTimeField()
    fecha_salida_real = models.DateTimeField(null=True, blank=True)
    fecha_llegada_real = models.DateTimeField(null=True, blank=True)
    terminal_salida = models.CharField(max_length=20, blank=True)
    gate_salida = models.CharField(max_length=10, blank=True)
    terminal_llegada = models.CharField(max_length=20, blank=True)
    gate_llegada = models.CharField(max_length=10, blank=True)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    asientos_disponibles = models.IntegerField()
    duracion_minutos = models.IntegerField()
    api_flight_iata = models.CharField(max_length=20)
    api_flight_icao = models.CharField(max_length=20)
    codeshare_info = models.CharField(max_length=50, blank=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

# --- Asiento ---
class Asiento(models.Model):
    vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE, related_name='asientos')
    numero_asiento = models.CharField(max_length=5)  # Ej: "12A"
    fila = models.IntegerField()
    columna = models.CharField(max_length=1)
    clase = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50, blank=True)
    precio_adicional = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    disponible = models.BooleanField(default=True)
    from django.conf import settings
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='asientos_reservados')
    created_at = models.DateTimeField(auto_now_add=True)
