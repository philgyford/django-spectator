from django.conf import settings


# e.g. "8 Apr 2018"
DATE_FORMAT = getattr(settings, 'SPECTATOR_READING_DATE_FORMAT', '%-d %b %Y')

# e.g. "2018"
DATE_YEAR_FORMAT = getattr(settings, 'SPECTATOR_READING_DATE_YEAR_FORMAT', '%Y')

# e.g. "Apr"
DATE_MONTH_FORMAT = getattr(settings, 'SPECTATOR_READING_DATE_YEAR_FORMAT', '%b')

# e.g. "8"
DATE_DAY_FORMAT = getattr(settings, 'SPECTATOR_READING_DATE_YEAR_FORMAT', '%-d')

# e.g. "Apr 2018"
DATE_YEAR_MONTH_FORMAT = getattr(settings, 'SPECTATOR_READING_DATE_YEAR_FORMAT', '%b %Y')

# e.g. "8 Apr"
DATE_MONTH_DAY_FORMAT = getattr(settings, 'SPECTATOR_READING_DATE_YEAR_FORMAT', '%-d %b')

# e.g. "2017–2018"
PERIOD_FORMAT_SHORT = getattr(settings, 'SPECTATOR_READING_PERIOD_FORMAT_SHORT', '{}–{}')

# e.g. "8 Apr to 2 May 2018"
PERIOD_FORMAT_LONG = getattr(settings, 'SPECTATOR_READING_PERIOD_FORMAT_LONG', '{} to {}')
