from django.apps import AppConfig

class VuelosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.vuelos'

    def ready(self):
        import apps.vuelos.signals  # Activa los signals al arrancar la app
