from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('ingreso/', views.ingreso, name='ingreso'),
    path('salir/', views.salir, name='salir'),
]
