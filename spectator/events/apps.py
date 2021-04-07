from django.apps import AppConfig


class SpectatorEventsAppConfig(AppConfig):
    label = "spectator_events"
    name = "spectator.events"
    verbose_name = "Spectator Events"

    # Maintain pre Django 3.2 default behaviour:
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        import spectator.events.signals  # noqa: F401
