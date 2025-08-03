from django.contrib import admin
from django.urls import path, include
#CORONA GARCIA CHRISTIAN JAVIER
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Vuelos_reservas.apps.usuarios.urls')),  #  app de usuarios
    path('vuelos/', include('Vuelos_reservas.apps.vuelos.urls')),  #  app de vuelos
    path('reservas/', include('Vuelos_reservas.apps.reservas.urls')),  # app de reservas
    path('api/', include('Vuelos_reservas.apps.api_nativa.urls')),  # la API nativa
    
]
