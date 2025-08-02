from django.contrib import admin
from django.urls import path, include
#CORONA GARCIA CHRISTIAN JAVIER
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.usuarios.urls')),  # Enrutas a tu app de usuarios
    path('vuelos/', include('apps.vuelos.urls')),  # Enruta a la app de vuelos
    path('reservas/', include('apps.reservas.urls')),  # Enruta a la app de reservas
    path('api/', include('apps.api_nativa.urls')),  # Enruta a la API nativa
    #path('accounts/', include('django.contrib.auth.urls')),   Rutas de login/logout por defecto
]
