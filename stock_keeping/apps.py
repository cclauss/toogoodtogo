from django.apps import AppConfig


class StockKeepingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stock_keeping'

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        # noinspection PyUnresolvedReferences
        from . import signals
