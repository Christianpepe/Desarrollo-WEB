# Aquí irán las vistas/endpoints de la API nativa de vuelos
#CORONA GARCIA CHRISTIAN JAVIER
from rest_framework import generics
from apps.vuelos.models import Vuelo
from .serializers import VueloSerializer

class VueloListView(generics.ListAPIView):
    queryset = Vuelo.objects.all()
    serializer_class = VueloSerializer
