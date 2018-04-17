from django.conf import settings


# e.g. "8 Apr 2018"
DATE_FORMAT = getattr(settings, 'SPECTATOR_EVENTS_DATE_FORMAT', '%-d %b %Y')
