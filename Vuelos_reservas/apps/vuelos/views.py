# --- Vista para reservar asiento ---
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@login_required
@require_POST
def reservar_asiento(request, vuelo_id):
    import json
    from apps.vuelos.models import Asiento, Vuelo
    user = request.user
    data = json.loads(request.body)
    numero_asiento = data.get('numero_asiento')
    print(f"[DEBUG] Usuario: {user}, Vuelo ID: {vuelo_id}, Numero asiento recibido: {numero_asiento}")
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    asiento = Asiento.objects.filter(vuelo=vuelo, numero_asiento=numero_asiento).first()
    print(f"[DEBUG] Asiento encontrado: {asiento}")
    if not asiento:
        print("[DEBUG] Asiento no encontrado en la base de datos.")
        return JsonResponse({'success': False, 'error': 'Asiento no encontrado.'}, status=404)
    if not asiento.disponible or asiento.usuario is not None:
        print(f"[DEBUG] Asiento ya ocupado. Disponible: {asiento.disponible}, Usuario: {asiento.usuario}")
        return JsonResponse({'success': False, 'error': 'Asiento ya ocupado.'}, status=400)
    # Verifica si el usuario ya reservó un asiento en este vuelo
    if Asiento.objects.filter(vuelo=vuelo, usuario=user).exists():
        print("[DEBUG] El usuario ya tiene un asiento reservado en este vuelo.")
        return JsonResponse({'success': False, 'error': 'Ya tienes un asiento reservado en este vuelo.'}, status=400)
    asiento.disponible = False
    asiento.usuario = user
    asiento.save(update_fields=["disponible", "usuario"])
    print(f"[DEBUG] Asiento actualizado y guardado. Disponible: {asiento.disponible}, Usuario: {asiento.usuario}")
    return JsonResponse({'success': True, 'asiento': asiento.numero_asiento})
# apps/vuelos/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils import timezone
from apps.vuelos.models import Vuelo, Aeropuerto, Asiento

# --- Vista de búsqueda de vuelos ---
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

# --- API de autocompletado de aeropuertos ---
@require_GET
def autocompletar_aeropuertos(request):
    q = request.GET.get('q', '').strip()
    if q:
        aeropuertos = Aeropuerto.objects.filter(
            Q(nombre__icontains=q) | Q(codigo_iata__icontains=q)
        )[:10]
        resultados = [f"{a.codigo_iata} - {a.nombre}" for a in aeropuertos]
    else:
        resultados = []
    return JsonResponse(resultados, safe=False)

# --- Vista de inicio ---
def inicio(request):
    ahora = timezone.now()
    vuelos_disponibles = Vuelo.objects.filter(
        fecha_salida_programada__gte=ahora
    ).order_by('fecha_salida_programada')[:10]
    context = {
        'vuelos_disponibles': vuelos_disponibles
    }
    return render(request, 'inicio.html', context)

# --- Vista de todos los vuelos ---
def vuelos_disponibles(request):
    vuelos = Vuelo.objects.select_related(
        'aerolinea', 'aeropuerto_origen', 'aeropuerto_destino'
    ).order_by('fecha_salida_programada')
    context = {
        'todos_vuelos': vuelos
    }
    return render(request, 'vuelos/lista_vuelos.html', context)

# apps/vuelos/views.py - Función detalle_vuelo actualizada

# apps/vuelos/views.py - Función detalle_vuelo actualizada

def detalle_vuelo(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    import random
    from django.contrib.auth.decorators import login_required
    asientos = list(Asiento.objects.filter(vuelo=vuelo).order_by('fila', 'columna'))
    # Si todos los asientos están disponibles y sin usuario, poblar ocupados solo una vez por vuelo
    if all(a.disponible and a.usuario is None for a in asientos):
        total = len(asientos)
        n_ocupados = random.randint(max(1, total // 10), max(1, total // 3))
        ocupados = random.sample(asientos, n_ocupados)
        for a in ocupados:
            a.disponible = False
            a.usuario = None
        Asiento.objects.bulk_update(ocupados, ["disponible", "usuario"])
    
   
    posiciones = {}
    filas = 14
    columnas = ['A', 'B', 'C', 'D']
    top_inicial = 15
    top_incremento = 6.25
    lefts = {
        'A': 35.7,
        'B': 41.7,
        'C': 54.0,
        'D': 60.0
    }
    # Posiciones para escritorio (por defecto)
    for fila in range(1, filas+1):
        top = top_inicial + (fila-1)*top_incremento
        for col in columnas:
            key = f"{fila}{col}"
            left = lefts[col]
            posiciones[key] = {"top": f"{top}%", "left": f"{left}%"}

    # Ejemplo de posiciones para la primera fila en móvil (puedes extender para las demás filas)
    posiciones_mobile = {
        "1A": {"top": "0%", "left": "0%"},
        "1B": {"top": "8%", "left": "38%"},
        "1C": {"top": "8%", "left": "58%"},
        "1D": {"top": "8%", "left": "68%"},
        
    }
   
    user = request.user if request.user.is_authenticated else None
    for asiento in asientos:
        asiento.posicion = posiciones.get(asiento.numero_asiento, {"top": "0px", "left": "0px"})
        # Marcar el estado visual para el template
        if asiento.usuario and user and asiento.usuario == user:
            asiento.estado_reserva = "propio"
        elif asiento.usuario and (not user or asiento.usuario != user):
            asiento.estado_reserva = "ocupado"
        elif not asiento.disponible:
            asiento.estado_reserva = "ocupado"
        else:
            asiento.estado_reserva = "disponible"
    
    context = {
        'vuelo': vuelo,
        'asientos': asientos
    }
    
    return render(request, 'vuelos/detalle_vuelo.html', context)