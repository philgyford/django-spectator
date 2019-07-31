from django.conf import settings


# Creating all the defaults for settings.
# In our code, if we want to use a SPECTATOR_EVENTS_* setting we should import
# from here, not django.conf.settings.


EVENTS_DIR_BASE = getattr(settings, 'SPECTATOR_EVENTS_DIR_BASE', 'events')
