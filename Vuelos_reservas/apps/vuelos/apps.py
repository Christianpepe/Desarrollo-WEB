from django.apps import AppConfig
#CORONA GARCIA CHRISTIAN JAVIER
class VuelosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Vuelos_reservas.apps.vuelos''

    def ready(self):
        import apps.vuelos.signals  # Activa los signals al arrancar la app
