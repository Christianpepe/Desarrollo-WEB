# Aquí se definirán las rutas de la API nativa de vuelos
from django.urls import path
from .views import VueloListView

urlpatterns = [
    path('vuelos/', VueloListView.as_view(), name='vuelos-list'),
]
