from django.apps import AppConfig


class HistoriqueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.historique'

    def ready(self):
        import backend.historique.signals
