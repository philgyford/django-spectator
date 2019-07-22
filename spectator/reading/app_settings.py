from django.conf import settings


# Creating all the defaults for settings.
# In our code, if we want to use a SPECTATOR_READING_* setting we should import
# from here, not django.conf.settings.


READING_DIR_BASE = getattr(settings, 'SPECTATOR_READING_DIR_BASE', 'reading')
