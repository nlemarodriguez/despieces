from django.apps import AppConfig


class QuotationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.quotations'
    verbose_name = 'Cotizaciones'

    def ready(self):
        import apps.quotations.signals
