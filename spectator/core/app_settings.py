from django.conf import settings


# Creating all the defaults for settings.
# In our code, if we want to use a SPECTATOR_* setting we should import
# from here, not django.conf.settings.

# Default:
MAPS = {"enable": False}

# Handle legacy version where we only have this map setting:
GOOGLE_MAPS_API_KEY = getattr(settings, "SPECTATOR_GOOGLE_MAPS_API_KEY", "")
if GOOGLE_MAPS_API_KEY:
    MAPS = {"enable": True, "library": "google", "api_key": GOOGLE_MAPS_API_KEY}

elif getattr(settings, "SPECTATOR_MAPS", False):
    # Or get the full dict setting if it exists:
    MAPS = getattr(settings, "SPECTATOR_MAPS")


# The characters to use for things that require an automatically-generated
# URL slug:
SLUG_ALPHABET = getattr(
    settings, "SPECTATOR_SLUG_ALPHABET", "abcdefghijkmnopqrstuvwxyz23456789"
)

# The salt value to use when generating URL slugs:
SLUG_SALT = getattr(settings, "SPECTATOR_SLUG_SALT", "Django Spectator")

# For Events and card titles.
DATE_FORMAT = getattr(settings, "SPECTATOR_DATE_FORMAT", "%-d %b %Y")

# For Reading and Events
THUMBNAIL_DETAIL_SIZE = getattr(settings, "SPECTATOR_THUMBNAIL_DETAIL_SIZE", (320, 320))

THUMBNAIL_LIST_SIZE = getattr(settings, "SPECTATOR_THUMBNAIL_LIST_SIZE", (80, 160))
