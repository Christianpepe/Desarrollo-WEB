from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.usuarios.urls')),  # Enrutas a tu app de usuarios
    path('vuelos/', include('apps.vuelos.urls')),  # Enruta a la app de vuelos
    path('reservas/', include('apps.reservas.urls')),  # Enruta a la app de reservas
   
    
]
