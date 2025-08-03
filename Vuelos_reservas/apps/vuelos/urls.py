# urls.py: Rutas de la app de vuelos
from django.urls import path
from . import views
from . import views_test
#CORONA GARCIA CHRISTIAN JAVIER
urlpatterns = [
    # Búsqueda de vuelos
    path('buscar-vuelos/', views.buscar_vuelos, name='buscar_vuelos'),

    # API de autocompletado de aeropuertos
    path('api/autocompletar-aeropuertos/', views.autocompletar_aeropuertos, name='autocompletar_aeropuertos'),

    # Lista de todos los vuelos disponibles
    path('vuelos/', views.vuelos_disponibles, name='lista_vuelos'),

    # Detalle de un vuelo específico
    path('vuelos/<int:vuelo_id>/', views.detalle_vuelo, name='detalle_vuelo'),

    # Reservar asiento (AJAX)
    path('vuelos/<int:vuelo_id>/reservar-asiento/', views.reservar_asiento, name='reservar_asiento'),

    # Página de agradecimiento tras reservar
    path('agradecimiento-reserva/', views.agradecimiento_reserva, name='agradecimiento_reserva'),
    # Recomendaciones de vuelos
    path('recomendaciones/', views.recomendaciones_vuelos, name='recomendaciones_vuelos'),
    # Conócenos
    path('conocenos/', views.conocenos, name='conocenos'),
    # Políticas de Privacidad
    path('politicas_privacidad/', views.politicas_privacidad, name='politicas_privacidad'),
    path('run-scheduler-test/', views_test.run_scheduler_test, name='run_scheduler_test'),
]
