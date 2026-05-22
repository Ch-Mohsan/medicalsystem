from django.apps import AppConfig


class MediconnectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myproject.Mediconnect'

    def ready(self):
        # Register system checks
        try:
            from . import checks  # noqa: F401
        except Exception:
            # Avoid crashing app startup if checks import fails
            pass
