from django.urls import path
from . import views
# Este archivo define las URLs para la aplicación de usuarios.
urlpatterns = [
    path('', views.inicio, name='inicio'),  # Página principal
    path('registro/', views.registro, name='registro'),
    path('ingreso/', views.ingreso, name='ingreso'),
    path('salir/', views.salir, name='salir'),
]
