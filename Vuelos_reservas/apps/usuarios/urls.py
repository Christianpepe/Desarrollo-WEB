
# Este archivo define las URLs para  usuarios:
# registro, ingreso , inicio y cierre de sesión.
#CORONA GARCIA CHRISTIAN JAVIER
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Página principal de usuario autenticado
    path('registro/', views.registro, name='registro'),  # Registro de usuario
    path('ingreso/', views.ingreso, name='ingreso'),      # Login de usuario
    path('salir/', views.salir, name='salir'),
  
]
