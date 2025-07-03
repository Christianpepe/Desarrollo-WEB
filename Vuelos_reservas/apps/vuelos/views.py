
# views.py: Vistas principales para la app de vuelos
# -----------------------------------------------
# Este archivo contiene las vistas principales para la gestión y consulta de vuelos.
# Incluye búsqueda, autocompletado, listado y detalle de vuelos.
# -----------------------------------------------

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils import timezone
from apps.vuelos.models import Vuelo, Aeropuerto

# --- Vista de búsqueda de vuelos ---
def buscar_vuelos(request):
    """
    Vista para buscar vuelos por origen, destino y fecha de salida.
    Permite filtrar vuelos según los parámetros recibidos por GET.
    """
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

# --- API de autocompletado de aeropuertos ---
@require_GET
def autocompletar_aeropuertos(request):
    """
    API para autocompletar aeropuertos por nombre o código IATA.
    Devuelve una lista de coincidencias para autocompletar en formularios.
    """
    q = request.GET.get('q', '').strip()
    if q:
        aeropuertos = Aeropuerto.objects.filter(
            Q(nombre__icontains=q) | Q(codigo_iata__icontains=q)
        )[:10]
        resultados = [f"{a.codigo_iata} - {a.nombre}" for a in aeropuertos]
    else:
        resultados = []
    return JsonResponse(resultados, safe=False)

# --- Vista de inicio: muestra próximos vuelos ---
def inicio(request):
    """
    Vista de inicio: muestra los próximos 10 vuelos ordenados por fecha de salida.
    """
    ahora = timezone.now()
    vuelos_disponibles = Vuelo.objects.filter(fecha_salida_programada__gte=ahora).order_by('fecha_salida_programada')[:10]
    context = {
        'vuelos_disponibles': vuelos_disponibles
    }
    return render(request, 'inicio.html', context)

# --- Vista de todos los vuelos disponibles ---
def vuelos_disponibles(request):
    """
    Vista que muestra todos los vuelos disponibles, ordenados por fecha de salida.
    """
    vuelos = Vuelo.objects.select_related('aerolinea', 'aeropuerto_origen', 'aeropuerto_destino').order_by('fecha_salida_programada')
    context = {
        'todos_vuelos': vuelos,
    }
    return render(request, 'vuelos/lista_vuelos.html', context)

# --- Vista de detalle de vuelo ---
def detalle_vuelo(request, vuelo_id):
    """
    Vista de detalle para un vuelo específico.
    Muestra toda la información relevante de un vuelo.
    """
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    context = {'vuelo': vuelo}
    return render(request, 'vuelos/detalle_vuelo.html', context)

# views.py: Vistas principales para la app de vuelos
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils import timezone
from apps.vuelos.models import Vuelo, Aeropuerto

def buscar_vuelos(request):
    """
    Vista para buscar vuelos por origen, destino y fecha de salida.
    """
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
    """
    API para autocompletar aeropuertos por nombre o código IATA.
    """
    q = request.GET.get('q', '').strip()
    if q:
        aeropuertos = Aeropuerto.objects.filter(
            Q(nombre__icontains=q) | Q(codigo_iata__icontains=q)
        )[:10]
        resultados = [f"{a.codigo_iata} - {a.nombre}" for a in aeropuertos]
    else:
        resultados = []
    return JsonResponse(resultados, safe=False)

def inicio(request):
    """
    Vista de inicio: muestra los próximos 10 vuelos ordenados por fecha de salida.
    """
    ahora = timezone.now()
    vuelos_disponibles = Vuelo.objects.filter(fecha_salida_programada__gte=ahora).order_by('fecha_salida_programada')[:10]
    context = {
        'vuelos_disponibles': vuelos_disponibles
    }
    return render(request, 'inicio.html', context)

def vuelos_disponibles(request):
    """
    Vista que muestra todos los vuelos disponibles, ordenados por fecha de salida.
    """
    vuelos = Vuelo.objects.select_related('aerolinea', 'aeropuerto_origen', 'aeropuerto_destino').order_by('fecha_salida_programada')
    context = {
        'todos_vuelos': vuelos,
    }
    return render(request, 'vuelos/lista_vuelos.html', context)

def detalle_vuelo(request, vuelo_id):
    """
    Vista de detalle para un vuelo específico.
    """
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    context = {'vuelo': vuelo}
    return render(request, 'vuelos/detalle_vuelo.html', context)


