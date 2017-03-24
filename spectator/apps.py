from django.apps import AppConfig


class SpectatorAppConfig(AppConfig):
    name = 'spectator'
    verbose_name = 'Spectator'

    def ready(self):
        import spectator.signals

