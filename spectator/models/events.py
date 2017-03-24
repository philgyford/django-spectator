# coding: utf-8
import datetime

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
try:
    # Django >= 1.10
    from django.urls import reverse
except ImportError:
    # Django < 1.10
    from django.core.urlresolvers import reverse

from polymorphic.models import PolymorphicModel

from . import BaseRole, Creator, TimeStampedModelMixin
from ..fields import NaturalSortField


class Event(TimeStampedModelMixin, PolymorphicModel):
    """
    Parent class for different kinds of event: Concert, MovieEvent, PlayEvent.

    A child class can add its own fields.
    """
    date = models.DateField(null=True, blank=False)
    venue = models.ForeignKey('Venue', blank=False)

    # Child classes should set their own unique value for event_kind:
    event_kind = 'event'

    class Meta:
        ordering = ['date',]

    def __str__(self):
        return 'Event #{}'.format(self.pk)


class ConcertRole(BaseRole):
    """
    Through model for linking a creator to a Concert, optionally via their role
    (e.g. 'Headliner', 'Support', etc.)

    Every time one of these is saved/deleted a signal re-saves the Concert
    in case its `title_sort` needs to change.
    """
    creator = models.ForeignKey('Creator', blank=False,
                        on_delete=models.CASCADE, related_name='concert_roles')

    concert = models.ForeignKey('Concert', on_delete=models.CASCADE,
                                                        related_name='roles')


class Concert(Event):
    """
    A gig.

    Get a Concert's creators:

        concert = Concert.objects.get(pk=1)

        # Just the creators:
        for creator in concert.creators.all():
            print(creator.name)

        # Include their roles:
        for role in concert.roles.all():
            print(role.concert, role.creator, role.role_name)
    """
    title = models.CharField(null=False, blank=True, max_length=255,
            help_text="Optional. e.g., 'Indietracks 2017', 'Radio 1 Roadshow'.")

    title_sort = NaturalSortField('title_to_sort', max_length=255, default='',
            help_text="e.g. 'reading festival, the' or 'drifters, the'.")

    creators = models.ManyToManyField(Creator, through='ConcertRole',
                                                    related_name='concerts')
    event_kind = 'concert'

    class Meta:
        ordering = ('title_sort',)

    def __str__(self):
        if self.title:
            return self.title
        else:
            roles = list(self.roles.all())
            if len(roles) == 0:
                return 'Concert #{}'.format(self.pk)
            elif len(roles) == 1:
                return str(roles[0].creator.name)
            else:
                roles = [r.creator.name for r in roles]
                # Join with commas but 'and' for the last one:
                return '{} and {}'.format(
                            ', '.join(roles[:-1]),
                            roles[-1]
                        )

    def get_absolute_url(self):
        return reverse('spectator:concert_detail', kwargs={'pk':self.pk})

    @property
    def title_to_sort(self):
        """
        The string we use to create the title_sort property.
        We want to be able to sort by the concert's Creators, if it doesn't
        have a title.
        """
        return self.__str__()


class MovieRole(BaseRole):
    """
    Through model for linking a creator to a Movie, optionally via their role
    (e.g.  'Director', 'Actor', etc.)
    """
    creator = models.ForeignKey('Creator', blank=False,
                        on_delete=models.CASCADE, related_name='movie_roles')

    movie = models.ForeignKey('Movie', on_delete=models.CASCADE,
                                                        related_name='roles')


class Movie(TimeStampedModelMixin, models.Model):
    """
    A movie itself, not an occasion on which it was watched.

    Get a Movie's creators:

        movie = Movie.objects.get(pk=1)

        # Just the creators:
        for creator in movie.creators.all():
            print(creator.name)

        # Include their roles:
        for role in movie.roles.all():
            print(role.movie, role.creator, role.role_name)

        # When it's been seen:
        for ev in movie.movieevent_set.all():
            print(ev.venue, ev.date)
    """
    YEAR_CHOICES = [(r,r) for r in range(1888, datetime.date.today().year+1)]
    YEAR_CHOICES.insert(0, ('', 'Select…'))

    title = models.CharField(null=False, blank=False, max_length=255)

    title_sort = NaturalSortField('title', max_length=255, default='',
            help_text="e.g. 'haine, la' or 'unbelievable truth, the'.")

    creators = models.ManyToManyField(Creator, through='MovieRole',
                                                        related_name='movies')

    imdb_id = models.CharField(null=False, blank=True, max_length=12,
                    verbose_name='IMDb ID',
                    help_text="Starts with 'tt', e.g. 'tt0100842'.",
                    validators=[
                        RegexValidator(
                            regex='^tt\d{7,10}$',
                            message='IMDb ID should be like "tt1234567"',
                            code='invalid_imdb_id'
                        )
                    ]
                )

    year = models.PositiveSmallIntegerField(null=True, blank=True,
                default=None,
                help_text="Year of release.")

    class Meta:
        ordering = ('title_sort',)

    def __str__(self):
        if self.year:
            return '{} ({})'.format(self.title, self.year)
        else:
            return self.title

    def get_absolute_url(self):
        return reverse('spectator:movie_detail', kwargs={'pk':self.pk})


class MovieEvent(Event):
    """
    An occasion on which a Movie was watched.
    """
    movie = models.ForeignKey('Movie', null=False, blank=False)
    event_kind = 'movie'

    def __str__(self):
        return str(self.movie)


class PlayRole(BaseRole):
    """
    Through model for linking a creator to a Play, optionally via their role
    (e.g. 'Author'.)
    """
    creator = models.ForeignKey('Creator', blank=False,
                        on_delete=models.CASCADE, related_name='play_roles')

    play = models.ForeignKey('Play', on_delete=models.CASCADE,
                                                        related_name='roles')


class Play(TimeStampedModelMixin, models.Model):
    """
    A play itself, not an occasion on which it was watched.

    Get a Play's creators:

        play = Play.objects.get(pk=1)

        # Just the creators:
        for creator in play.creators.all():
            print(creator.name)

        # Include their roles:
        for role in play.roles.all():
            print(role.play, role.creator, role.role_name)

        # The productions and events:
        for production in play.playproduction_set.all():
            print(production)
            for event in production.playproductionevent_set.all():
                print(event.venue, event.date)
    """
    title = models.CharField(null=False, blank=False, max_length=255)

    title_sort = NaturalSortField('title', max_length=255, default='',
            help_text="e.g. 'big play, a' or 'biggest play, the'.")

    creators = models.ManyToManyField(Creator, through='PlayRole',
                                                        related_name='plays')

    class Meta:
        ordering = ('title_sort',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('spectator:play_detail', kwargs={'pk':self.pk})


class PlayProductionRole(BaseRole):
    """
    Through model for linking a creator to a particular production of a Play,
    optionally via their role (e.g. 'Director' or 'Actor'.)
    """
    creator = models.ForeignKey('Creator', blank=False,
                on_delete=models.CASCADE, related_name='play_production_roles')

    production = models.ForeignKey('PlayProduction', on_delete=models.CASCADE,
                                                related_name='roles')


class PlayProduction(TimeStampedModelMixin, models.Model):
    """
    A particular production of a play by a certain company/director/etc.

    Get a PlayProduction's creators:

        production = PlayProduction.objects.get(pk=1)

        # Just the creators:
        for creator in production.creators.all():
            print(creator.name)

        # Include their roles:
        for role in production.roles.all():
            print(role.production.play, role.production.title,\
                    role.creator, role.role_name)

        # The events:
        for event in production.playproductionevent_set.all():
            print(event.venue, event.date)
    """
    play = models.ForeignKey('Play', null=False, blank=False)

    title = models.CharField(null=False, blank=True, max_length=255,
            help_text="Optional title of this production of the play.")

    creators = models.ManyToManyField('Creator', through='PlayProductionRole',
                    related_name='play_productions',
                    help_text="The director, actors, etc. in this production.")

    class Meta:
        ordering = ('play__title',)

    def __str__(self):
        if self.title:
            return self.title
        else:
            roles = list(self.roles.all())
            if len(roles) == 0:
                return 'Production of {}'.format(self.play)
            elif len(roles) == 1:
                return '{} by {}'.format(self.play, roles[0].creator)
            else:
                return '{} by {} et al.'.format(
                            self.play,
                            roles[0].creator.name
                        )


class PlayProductionEvent(Event):
    """
    An occasion on which a PlayProduction was watched.
    """
    production = models.ForeignKey('PlayProduction', blank=False)
    event_kind = 'play'

    def __str__(self):
        return str(self.production)


class MiscEventRole(BaseRole):
    """
    Through model for linking a creator to a MiscEvent, optionally via their
    role (e.g. 'Performer', 'Director', etc.)

    Every time one of these is saved/deleted a signal re-saves the MiscEvent
    in case its `title_sort` needs to change.
    """
    creator = models.ForeignKey('Creator', blank=False,
                    on_delete=models.CASCADE, related_name='miscevent_roles')

    miscevent = models.ForeignKey('MiscEvent', on_delete=models.CASCADE,
                                                        related_name='roles')


class MiscEvent(Event):

    title = models.CharField(null=False, blank=True, max_length=255,
            help_text="Optional. e.g., 'A Great Event'.")

    title_sort = NaturalSortField('title_to_sort', max_length=255, default='',
            help_text="e.g. 'great event, a'.")

    creators = models.ManyToManyField(Creator, through='MiscEventRole',
                                                    related_name='miscevents')
    event_kind = 'misc'

    class Meta:
        ordering = ('title_sort',)

    def __str__(self):
        if self.title:
            return self.title
        else:
            roles = list(self.roles.all())
            if len(roles) == 0:
                return 'Misc Event #{}'.format(self.pk)
            elif len(roles) == 1:
                return str(roles[0].creator.name)
            else:
                roles = [r.creator.name for r in roles]
                # Join with commas but 'and' for the last one:
                return '{} and {}'.format(
                            ', '.join(roles[:-1]),
                            roles[-1]
                        )

    def get_absolute_url(self):
        return reverse('spectator:miscevent_detail', kwargs={'pk':self.pk})

    @property
    def title_to_sort(self):
        """
        The string we use to create the title_sort property.
        We want to be able to sort by the concert's MiscEvent's, if it doesn't
        have a title.
        """
        return self.__str__()


class Venue(TimeStampedModelMixin, models.Model):
    """
    Where an event happens.
    """
    # From https://github.com/SmileyChris/django-countries/blob/master/django_countries/data.py
    # With those marked #changed being, er, changed.
    COUNTRIES = {
        "AF": _("Afghanistan"),
        "AX": _("Åland Islands"),
        "AL": _("Albania"),
        "DZ": _("Algeria"),
        "AS": _("American Samoa"),
        "AD": _("Andorra"),
        "AO": _("Angola"),
        "AI": _("Anguilla"),
        "AQ": _("Antarctica"),
        "AG": _("Antigua and Barbuda"),
        "AR": _("Argentina"),
        "AM": _("Armenia"),
        "AW": _("Aruba"),
        "AU": _("Australia"),
        "AT": _("Austria"),
        "AZ": _("Azerbaijan"),
        "BS": _("Bahamas"),
        "BH": _("Bahrain"),
        "BD": _("Bangladesh"),
        "BB": _("Barbados"),
        "BY": _("Belarus"),
        "BE": _("Belgium"),
        "BZ": _("Belize"),
        "BJ": _("Benin"),
        "BM": _("Bermuda"),
        "BT": _("Bhutan"),
        "BO": _("Bolivia (Plurinational State of)"),
        "BQ": _("Bonaire, Sint Eustatius and Saba"),
        "BA": _("Bosnia and Herzegovina"),
        "BW": _("Botswana"),
        "BV": _("Bouvet Island"),
        "BR": _("Brazil"),
        "IO": _("British Indian Ocean Territory"),
        "BN": _("Brunei Darussalam"),
        "BG": _("Bulgaria"),
        "BF": _("Burkina Faso"),
        "BI": _("Burundi"),
        "CV": _("Cabo Verde"),
        "KH": _("Cambodia"),
        "CM": _("Cameroon"),
        "CA": _("Canada"),
        "KY": _("Cayman Islands"),
        "CF": _("Central African Republic"),
        "TD": _("Chad"),
        "CL": _("Chile"),
        "CN": _("China"),
        "CX": _("Christmas Island"),
        "CC": _("Cocos (Keeling) Islands"),
        "CO": _("Colombia"),
        "KM": _("Comoros"),
        "CD": _("Congo (the Democratic Republic of the)"),
        "CG": _("Congo"),
        "CK": _("Cook Islands"),
        "CR": _("Costa Rica"),
        "CI": _("Côte d'Ivoire"),
        "HR": _("Croatia"),
        "CU": _("Cuba"),
        "CW": _("Curaçao"),
        "CY": _("Cyprus"),
        "CZ": _("Czechia"),
        "DK": _("Denmark"),
        "DJ": _("Djibouti"),
        "DM": _("Dominica"),
        "DO": _("Dominican Republic"),
        "EC": _("Ecuador"),
        "EG": _("Egypt"),
        "SV": _("El Salvador"),
        "GQ": _("Equatorial Guinea"),
        "ER": _("Eritrea"),
        "EE": _("Estonia"),
        "ET": _("Ethiopia"),
        "FK": _("Falkland Islands  [Malvinas]"),
        "FO": _("Faroe Islands"),
        "FJ": _("Fiji"),
        "FI": _("Finland"),
        "FR": _("France"),
        "GF": _("French Guiana"),
        "PF": _("French Polynesia"),
        "TF": _("French Southern Territories"),
        "GA": _("Gabon"),
        "GM": _("Gambia"),
        "GE": _("Georgia"),
        "DE": _("Germany"),
        "GH": _("Ghana"),
        "GI": _("Gibraltar"),
        "GR": _("Greece"),
        "GL": _("Greenland"),
        "GD": _("Grenada"),
        "GP": _("Guadeloupe"),
        "GU": _("Guam"),
        "GT": _("Guatemala"),
        "GG": _("Guernsey"),
        "GN": _("Guinea"),
        "GW": _("Guinea-Bissau"),
        "GY": _("Guyana"),
        "HT": _("Haiti"),
        "HM": _("Heard Island and McDonald Islands"),
        "VA": _("Holy See"),
        "HN": _("Honduras"),
        "HK": _("Hong Kong"),
        "HU": _("Hungary"),
        "IS": _("Iceland"),
        "IN": _("India"),
        "ID": _("Indonesia"),
        "IR": _("Iran (Islamic Republic of)"),
        "IQ": _("Iraq"),
        "IE": _("Ireland"),
        "IM": _("Isle of Man"),
        "IL": _("Israel"),
        "IT": _("Italy"),
        "JM": _("Jamaica"),
        "JP": _("Japan"),
        "JE": _("Jersey"),
        "JO": _("Jordan"),
        "KZ": _("Kazakhstan"),
        "KE": _("Kenya"),
        "KI": _("Kiribati"),
        "KP": _("Korea (the Democratic People's Republic of)"),
        "KR": _("Korea (the Republic of)"),
        "KW": _("Kuwait"),
        "KG": _("Kyrgyzstan"),
        "LA": _("Lao People's Democratic Republic"),
        "LV": _("Latvia"),
        "LB": _("Lebanon"),
        "LS": _("Lesotho"),
        "LR": _("Liberia"),
        "LY": _("Libya"),
        "LI": _("Liechtenstein"),
        "LT": _("Lithuania"),
        "LU": _("Luxembourg"),
        "MO": _("Macao"),
        "MK": _("Macedonia (the former Yugoslav Republic of)"),
        "MG": _("Madagascar"),
        "MW": _("Malawi"),
        "MY": _("Malaysia"),
        "MV": _("Maldives"),
        "ML": _("Mali"),
        "MT": _("Malta"),
        "MH": _("Marshall Islands"),
        "MQ": _("Martinique"),
        "MR": _("Mauritania"),
        "MU": _("Mauritius"),
        "YT": _("Mayotte"),
        "MX": _("Mexico"),
        "FM": _("Micronesia (Federated States of)"),
        "MD": _("Moldova (the Republic of)"),
        "MC": _("Monaco"),
        "MN": _("Mongolia"),
        "ME": _("Montenegro"),
        "MS": _("Montserrat"),
        "MA": _("Morocco"),
        "MZ": _("Mozambique"),
        "MM": _("Myanmar"),
        "NA": _("Namibia"),
        "NR": _("Nauru"),
        "NP": _("Nepal"),
        "NL": _("Netherlands"),
        "NC": _("New Caledonia"),
        "NZ": _("New Zealand"),
        "NI": _("Nicaragua"),
        "NE": _("Niger"),
        "NG": _("Nigeria"),
        "NU": _("Niue"),
        "NF": _("Norfolk Island"),
        "MP": _("Northern Mariana Islands"),
        "NO": _("Norway"),
        "OM": _("Oman"),
        "PK": _("Pakistan"),
        "PW": _("Palau"),
        "PS": _("Palestine, State of"),
        "PA": _("Panama"),
        "PG": _("Papua New Guinea"),
        "PY": _("Paraguay"),
        "PE": _("Peru"),
        "PH": _("Philippines"),
        "PN": _("Pitcairn"),
        "PL": _("Poland"),
        "PT": _("Portugal"),
        "PR": _("Puerto Rico"),
        "QA": _("Qatar"),
        "RE": _("Réunion"),
        "RO": _("Romania"),
        "RU": _("Russian Federation"),
        "RW": _("Rwanda"),
        "BL": _("Saint Barthélemy"),
        "SH": _("Saint Helena, Ascension and Tristan da Cunha"),
        "KN": _("Saint Kitts and Nevis"),
        "LC": _("Saint Lucia"),
        "MF": _("Saint Martin (French part)"),
        "PM": _("Saint Pierre and Miquelon"),
        "VC": _("Saint Vincent and the Grenadines"),
        "WS": _("Samoa"),
        "SM": _("San Marino"),
        "ST": _("Sao Tome and Principe"),
        "SA": _("Saudi Arabia"),
        "SN": _("Senegal"),
        "RS": _("Serbia"),
        "SC": _("Seychelles"),
        "SL": _("Sierra Leone"),
        "SG": _("Singapore"),
        "SX": _("Sint Maarten (Dutch part)"),
        "SK": _("Slovakia"),
        "SI": _("Slovenia"),
        "SB": _("Solomon Islands"),
        "SO": _("Somalia"),
        "ZA": _("South Africa"),
        "GS": _("South Georgia and the South Sandwich Islands"),
        "SS": _("South Sudan"),
        "ES": _("Spain"),
        "LK": _("Sri Lanka"),
        "SD": _("Sudan"),
        "SR": _("Suriname"),
        "SJ": _("Svalbard and Jan Mayen"),
        "SZ": _("Swaziland"),
        "SE": _("Sweden"),
        "CH": _("Switzerland"),
        "SY": _("Syrian Arab Republic"),
        "TW": _("Taiwan (Province of China)"),
        "TJ": _("Tajikistan"),
        "TZ": _("Tanzania, United Republic of"),
        "TH": _("Thailand"),
        "TL": _("Timor-Leste"),
        "TG": _("Togo"),
        "TK": _("Tokelau"),
        "TO": _("Tonga"),
        "TT": _("Trinidad and Tobago"),
        "TN": _("Tunisia"),
        "TR": _("Turkey"),
        "TM": _("Turkmenistan"),
        "TC": _("Turks and Caicos Islands"),
        "TV": _("Tuvalu"),
        "UG": _("Uganda"),
        "UA": _("Ukraine"),
        "AE": _("United Arab Emirates"),
        "GB": _("UK"), #changed
        "UM": _("United States Minor Outlying Islands"),
        "US": _("USA"), #changed
        "UY": _("Uruguay"),
        "UZ": _("Uzbekistan"),
        "VU": _("Vanuatu"),
        "VE": _("Venezuela (Bolivarian Republic of)"),
        "VN": _("Viet Nam"),
        "VG": _("Virgin Islands (British)"),
        "VI": _("Virgin Islands (U.S.)"),
        "WF": _("Wallis and Futuna"),
        "EH": _("Western Sahara"),
        "YE": _("Yemen"),
        "ZM": _("Zambia"),
        "ZW": _("Zimbabwe"),
    }

    COUNTRY_CHOICES = [(k,v) for k,v in COUNTRIES.items()]

    name = models.CharField(null=False, blank=False, max_length=255)

    name_sort = NaturalSortField('name', max_length=255, default='',
            help_text="e.g. 'venue, a' or 'biggest venue, the'.")

    latitude = models.DecimalField(max_digits=9, decimal_places=6,
                                                        null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,
                                                        null=True, blank=True)

    address = models.CharField(null=False, blank=True, max_length=255)

    country = models.CharField(null=False, blank=True, max_length=2,
                    choices=COUNTRY_CHOICES,
                    help_text="The ISO 3166-1 alpha-2 code, e.g. 'GB' or 'FR'")

    class Meta:
        ordering = ['name_sort',]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('spectator:venue_detail', kwargs={'pk':self.pk})

    @property
    def country_name(self):
        if self.country:
            return self.COUNTRIES[self.country]
        else:
            return None

