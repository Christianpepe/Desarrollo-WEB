from django.urls import path
from Vuelos_reservas.apps.reservas.views import mis_reservas
#CORONA GARCIA CHRISTIAN JAVIER
urlpatterns = [
    path('mis-reservas/', mis_reservas, name='mis_reservas'),
]
