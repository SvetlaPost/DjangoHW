from django.apps import AppConfig


class SecondAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'second_app'

    def ready(self):
        import second_app.signals
