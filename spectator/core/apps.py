from django.apps import apps, AppConfig


class SpectatorCoreAppConfig(AppConfig):
    label = 'spectator_core'
    name = 'spectator.core'
    verbose_name = 'Spectator Core'


class Apps(object):
    """Methods for seeing which Spectator apps are installed/enabled.
    At the moment installed is the same as enabled, but in future we may add
    conditions that mean an installed app can be disabled.

    So use installed to check if the code is physically in INSTALLED_APPS.
    And use enabled to check if we're allowed to use that app on the site.
    """

    def all(self):
        "A list of all possible Spectator apps that could be installed/enabled."
        return [
                'events',
                'reading',
               ]

    def installed(self):
        "A list of all the installed Spectator apps."
        return [app for app in self.all() if self.is_installed(app)]

    def enabled(self):
        "A list of all the enabled Spectator apps."
        return [app for app in self.all() if self.is_enabled(app)]

    def is_installed(self, app_name):
        "Is this Spectator app installed?"
        return apps.is_installed('spectator.%s' % app_name)

    def is_enabled(self, app_name):
        """Determine if a particular Spectator app is installed and enabled.

        app_name is like 'events' or 'reading'.

        Usage:
            if is_enabled('events'):
                print("Events is enabled")

        Doesn't offer much over apps.is_installed() yet, but would let us add
        other conditions in future, like being able to enable/disable installed
        apps.
        """
        return apps.is_installed('spectator.%s' % app_name)


spectator_apps = Apps()

