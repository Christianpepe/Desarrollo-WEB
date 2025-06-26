from django.urls import path
from . import views
# This file defines the URL patterns for the vuelos app, mapping the 'buscar-vuelos/' path to the buscar_vuelos view.
# It imports the necessary modules and the views from the current package, ensuring that the buscar_vuelos function is called when the specified URL is accessed.
# The urlpatterns list contains the URL patterns for the app, allowing Django to route requests to the appropriate view functions.

urlpatterns = [
    path('buscar-vuelos/', views.buscar_vuelos, name='buscar_vuelos'),
    path('api/autocompletar-aeropuertos/', views.autocompletar_aeropuertos, name='autocompletar_aeropuertos'),

]
