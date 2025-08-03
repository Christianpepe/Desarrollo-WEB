from django.urls import path
#CORONA GARCIA CHRISTIAN JAVIER
urlpatterns = [
    path('mis-reservas/', __import__('Vuelos_reservas.apps.reservas.views').reservas.views.mis_reservas, name='mis_reservas'),
]
