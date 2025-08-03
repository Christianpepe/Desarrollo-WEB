from django.contrib import admin
from django.urls import path, include
#CORONA GARCIA CHRISTIAN JAVIER
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Vuelos_reservas.apps.usuarios.urls')),  # Enrutas a tu app de usuarios
    path('vuelos/', include('Vuelos_reservas.apps.vuelos.urls')),  # Enruta a la app de vuelos
    path('reservas/', include('Vuelos_reservas.apps.reservas.urls')),  # Enruta a la app de reservas
    path('api/', include('Vuelos_reservas.apps.api_nativa.urls')),  # Enruta a la API nativa
    #path('accounts/', include('django.contrib.auth.urls')),   Rutas de login/logout por defecto
]
