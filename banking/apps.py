from django.apps import AppConfig


class BankingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'banking'

    # Import signals to connect them
    # ----------------------------------------------------
    def ready(self):
        from . import signals 