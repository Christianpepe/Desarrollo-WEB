# scripts/actualizar_fk_vuelos.py
import os
import sys
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from Vuelos_reservas.apps.vuelos.models import Vuelo, Aeropuerto

# Actualiza los FK de aeropuerto_origen y aeropuerto_destino en vuelos

def actualizar_fk_vuelos():
    print('Actualizando FK de aeropuerto_origen y aeropuerto_destino en vuelos...')
    icao_to_id = {a.codigo_icao: a.id for a in Aeropuerto.objects.all() if a.codigo_icao}
    vuelos_actualizados = 0
    for vuelo in Vuelo.objects.all():
        actualizado = False
        # Origen
        if vuelo.aeropuerto_origen_id:
            origen = Aeropuerto.objects.filter(id=vuelo.aeropuerto_origen_id).first()
            print(f"Vuelo {vuelo.id}: origen ICAO actual={origen.codigo_icao if origen else None}")
            if origen and origen.codigo_icao and origen.codigo_icao in icao_to_id and origen.id != icao_to_id[origen.codigo_icao]:
                vuelo.aeropuerto_origen_id = icao_to_id[origen.codigo_icao]
                actualizado = True
        # Destino
        if vuelo.aeropuerto_destino_id:
            destino = Aeropuerto.objects.filter(id=vuelo.aeropuerto_destino_id).first()
            print(f"Vuelo {vuelo.id}: destino ICAO actual={destino.codigo_icao if destino else None}")
            if destino and destino.codigo_icao and destino.codigo_icao in icao_to_id and destino.id != icao_to_id[destino.codigo_icao]:
                vuelo.aeropuerto_destino_id = icao_to_id[destino.codigo_icao]
                actualizado = True
        if actualizado:
            vuelo.save()
            vuelos_actualizados += 1
    print(f'✅ Vuelos actualizados: {vuelos_actualizados}')

if __name__ == '__main__':
    actualizar_fk_vuelos()
