# Este archivo contiene las vistas principales para el registro, autenticación
# y gestión de la sesión de usuarios en el sistema.
#CORONA GARCIA CHRISTIAN JAVIER

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from Vuelos_reservas.apps.vuelos.models import Vuelo
from django.utils import timezone
import requests
from django.conf import settings


#  Vista de registro de usuario
def registro(request):
    """
    Permite a un nuevo usuario registrarse en el sistema.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        hcaptcha_ok = validar_hcaptcha(request)
        if form.is_valid() and hcaptcha_ok:
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso. ¡Bienvenido!')
            return redirect('inicio')
        else:
            if not hcaptcha_ok:
                messages.error(request, "Verificación de seguridad fallida. Intenta de nuevo.")
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
        'hcaptcha_site_key': settings.HCAPTCHA_SITE_KEY
    }
    return render(request, 'registration/registro.html', context)

# login de usuario 
def ingreso(request):
    """
    Permite al usuario autenticarse en el sistema.
    """
    if request.method == 'POST':
        hcaptcha_ok = validar_hcaptcha(request)
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid() and hcaptcha_ok:
            user = form.get_user()
            login(request, user)
            messages.success(request, '¡Ingreso exitoso!')
            return redirect('inicio')
        else:
            if not hcaptcha_ok:
                messages.error(request, "Verificación de seguridad fallida. Intenta de nuevo.")
            messages.error(request, "Credenciales incorrectas.")
    else:
        form = CustomAuthenticationForm()
    context = {
        'form': form,
        'hcaptcha_site_key': settings.HCAPTCHA_SITE_KEY
    }
    return render(request, 'registration/ingreso.html', context)

def validar_hcaptcha(request):
    hcaptcha_response = request.POST.get('h-captcha-response')
    data = {
        'secret': settings.HCAPTCHA_SECRET_KEY,
        'response': hcaptcha_response
    }
    r = requests.post('https://hcaptcha.com/siteverify', data=data)
    result = r.json()
    return result.get('success', False)


#Vista de inicio para despues del login
@login_required
def inicio(request):
    """
    Muestra los próximos 10 vuelos reales disponibles para el usuario autenticado.
    Se priorizan los vuelos reales (con datos de la API).
    """
    ahora = timezone.now()
    vuelos_reales = Vuelo.objects.filter(
        fecha_salida_programada__gte=ahora
    ).exclude(api_flight_iata='', api_flight_icao='').order_by('fecha_salida_programada')[:10]
    context = {
        'vuelos_disponibles': vuelos_reales
    }
    return render(request, 'inicio.html', context)

# Vista para cerrar sesión
def salir(request):
    """
    Cierra la sesión del usuario y redirige a la página de ingreso.
    """
    logout(request)
    return redirect('ingreso')
