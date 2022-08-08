from django.apps import AppConfig


class SpectatorReadingAppConfig(AppConfig):
    label = "spectator_reading"
    name = "spectator.reading"
    verbose_name = "Spectator Reading"

    # Maintain pre Django 3.2 default behaviour:
    default_auto_field = "django.db.models.AutoField"
