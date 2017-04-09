from django.apps import AppConfig


class SpectatorEventsAppConfig(AppConfig):
    name = 'spectator.events'
    verbose_name = 'Spectator Events'

    def ready(self):
        import spectator.events.signals

