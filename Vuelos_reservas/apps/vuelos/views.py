from django.shortcuts import render
from django.db.models import Q
from apps.vuelos.models import Vuelo
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from apps.vuelos.models import Aeropuerto

def buscar_vuelos(request):
    origen = request.GET.get('origen', '').strip()
    destino = request.GET.get('destino', '').strip()
    fecha_salida = request.GET.get('fecha_salida', '')

    vuelos = Vuelo.objects.all()

    if origen:
        vuelos = vuelos.filter(aeropuerto_origen__nombre__icontains=origen)

    if destino:
        vuelos = vuelos.filter(aeropuerto_destino__nombre__icontains=destino)

    if fecha_salida:
        vuelos = vuelos.filter(fecha_salida_programada__date=fecha_salida)

    context = {
        'vuelos_encontrados': vuelos,
        'busqueda_realizada': True
    }

    return render(request, 'vuelos/resultados_busqueda.html', context)

@require_GET
def autocompletar_aeropuertos(request):
    q = request.GET.get('q', '').strip()

    if q:
        aeropuertos = Aeropuerto.objects.filter(
            Q(nombre__icontains=q) | Q(codigo_iata__icontains=q)
        )[:10]
        resultados = [
            f"{a.codigo_iata} - {a.nombre}" for a in aeropuertos
        ]
    else:
        resultados = []

    return JsonResponse(resultados, safe=False)
