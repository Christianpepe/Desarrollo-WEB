from Vuelos_reservas.apps.vuelos.models import Vuelo
from Vuelos_reservas.apps.vuelos.utils import generar_asientos_para_vuelo

# Script para regenerar asientos de todos los vuelos existentes

def run():
    print("Regenerando asientos para todos los vuelos...")
    for vuelo in Vuelo.objects.all():
        vuelo.asiento_set.all().delete()
        generar_asientos_para_vuelo(vuelo)
        print(f"Asientos generados para vuelo {vuelo.numero_vuelo}")
    print("Listo.")

if __name__ == "__main__":
    run()
