# Aquí se definirán los serializadores para la API nativa de vuelos
#CORONA GARCIA CHRISTIAN JAVIER
from rest_framework import serializers
from Vuelos_reservas.apps.vuelos.models import Vuelo

class VueloSerializer(serializers.ModelSerializer):
    duracion_estimada_horas = serializers.SerializerMethodField()

    class Meta:
        model = Vuelo
        fields = [
            'id', 'numero_vuelo', 'flight_date', 'aerolinea', 'aeropuerto_origen', 'aeropuerto_destino',
            'modelo_avion', 'flight_status', 'fecha_salida_programada', 'fecha_llegada_programada',
            'precio_base', 'duracion_minutos', 'duracion_estimada_horas', 'asientos_disponibles', 'terminal_salida', 'gate_salida',
            'terminal_llegada', 'gate_llegada', 'api_flight_iata', 'api_flight_icao', 'codeshare_info'
        ]

    def get_duracion_estimada_horas(self, obj):
        from .utils import estimar_precio_y_duracion
        vuelo_dict = {
            'codigo_vuelo': getattr(obj, 'numero_vuelo', ''),
            'origen': {'codigo_iata': getattr(obj.aeropuerto_origen, 'codigo_iata', '')} if obj.aeropuerto_origen else {},
            'destino': {'codigo_iata': getattr(obj.aeropuerto_destino, 'codigo_iata', '')} if obj.aeropuerto_destino else {},
            'modelo_avion': getattr(obj, 'modelo_avion', None),
        }
        fecha = getattr(obj, 'flight_date', None)
        vuelo_enriquecido = estimar_precio_y_duracion(vuelo_dict, fecha=fecha)
        return vuelo_enriquecido.get('duracion_estimada_horas', None)
