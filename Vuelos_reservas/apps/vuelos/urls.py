
# urls.py: Rutas de la app de vuelos
from django.urls import path
from . import views

urlpatterns = [
    # Búsqueda de vuelos
    path('buscar-vuelos/', views.buscar_vuelos, name='buscar_vuelos'),

    # API de autocompletado de aeropuertos
    path('api/autocompletar-aeropuertos/', views.autocompletar_aeropuertos, name='autocompletar_aeropuertos'),

    # Lista de todos los vuelos disponibles
    path('vuelos/', views.vuelos_disponibles, name='lista_vuelos'),

    # Detalle de un vuelo específico
    path('vuelos/<int:vuelo_id>/', views.detalle_vuelo, name='detalle_vuelo'),
]
