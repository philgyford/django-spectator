# coding: utf-8
import datetime

from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from spectator.core.models import BaseRole, SluggedModelMixin,\
        TimeStampedModelMixin
from spectator.core.fields import NaturalSortField
from spectator.core.utils import truncate_string


class EventRole(BaseRole):
    """
    Through model for linking a Creator to an Event, optionally via their role
    (e.g. 'Headliner', 'Support', 'Pianist', 'Actor', etc.)

    Every time one of these is saved/deleted a signal re-saves the Event
    in case its `title_sort` needs to change.
    """
    creator = models.ForeignKey('spectator_core.Creator', blank=False,
                        on_delete=models.CASCADE, related_name='event_roles')

    event = models.ForeignKey('spectator_events.Event', on_delete=models.CASCADE,
                                                        related_name='roles')

    class Meta:
        verbose_name = 'event role'
        ordering = ('role_order', 'role_name',)


class Event(TimeStampedModelMixin, SluggedModelMixin, models.Model):
    """
    A thing that happened at a particular venue on a particular date.

    You can get all the Event's Movies, Classical Works etc by doing:

        event = Event.objects.get(pk=1)

        event.classicalworks.all()
        event.dancepieces.all()
        event.movies.all()
        event.plays.all()

    But if there are more than one of a kind of Work, they won't necessarily
    be returned in the correct order, as defined in their through model. To
    return them in the correct order you need to use the selection. e.g.:

        event.classical_work_selections.all()
        event.dance_piece_selections.all()
        event.movie_selections.all()
        event.play_selections.all()

    Each item returned will then have an object associated, and an order. e.g.:

        selection = event.dance_piece_selections.first()
        print(selection.dance_piece.title)
        print(selection.order)

    Similarly, to get Creators who worked directly on the Event (as
    opposed to worked on one of its Works), in the correct order:

        event.roles.all()

    And access the Creators and the order like:

        role = event.roles.first()
        print(role.creator.name)
        print(role.role_order)
    """

    # The keys are used as slugs, so should be appropriate:
    KIND_CHOICES = (
        ('concert',     'Classical concert'),
        ('comedy',      'Comedy'),
        ('dance',       'Dance'),
        ('exhibition',  'Exhibition'),
        ('gig',         'Gig'),
        ('misc',        'Other'),
        ('movie',       'Movie'),
        ('play',        'Play'),
    )

    # Mapping keys from KIND_CHOICES to the slugs we'll use in URLs:
    KIND_SLUGS = {
        'comedy':       'comedy',
        'concert':      'concerts',
        'dance':        'dance',
        'exhibition':   'exhibitions',
        'gig':          'gigs',
        'misc':         'misc',
        'movie':        'movies',
        'play':         'plays'
    }

    kind = models.CharField(max_length=20, choices=KIND_CHOICES, blank=False)

    date = models.DateField(null=True, blank=False)

    venue = models.ForeignKey('spectator_events.Venue', null=True, blank=True,
                                                    on_delete=models.CASCADE)

    title = models.CharField(null=False, blank=True, max_length=255,
            help_text="Optional. e.g., 'Indietracks 2017', 'Radio 1 Roadshow'.")

    title_sort = NaturalSortField('title_to_sort', max_length=255, default='',
            help_text="e.g. 'reading festival, the' or 'drifters, the'.")

    note = models.TextField(null=False, blank=True,
        help_text="Optional. Paragraphs will be surrounded with &lt;p&gt;&lt;/p&gt; tags. HTML allowed.")

    creators = models.ManyToManyField('spectator_core.Creator',
                                through='EventRole', related_name='events')

    movies = models.ManyToManyField('spectator_events.Movie',
            through='spectator_events.MovieSelection',
            blank=True,
            help_text="Only used if event is of 'Movie' kind.")

    plays = models.ManyToManyField('spectator_events.Play',
            through='spectator_events.PlaySelection',
            blank=True,
            help_text="Only used if event is of 'Play' kind.")

    classicalworks = models.ManyToManyField('spectator_events.ClassicalWork',
            through='spectator_events.ClassicalWorkSelection',
            blank=True,
            help_text="Only used if event is of 'Classical Concert' kind.")

    dancepieces = models.ManyToManyField('spectator_events.DancePiece',
            through='spectator_events.DancePieceSelection',
            blank=True,
            help_text="Only used if event is of 'Dance' kind.")

    kind_slug = models.SlugField(null=False, blank=True,
            help_text="Set when the event is saved.")

    class Meta:
        ordering = ['-date',]

    def __str__(self):
        return self.make_title()

    def save(self, *args, **kwargs):
        self.kind_slug = self.KIND_SLUGS[self.kind]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('spectator:events:event_detail', kwargs={'slug':self.slug})

    def make_title(self):
        if self.title == '':
            title_start = Event.get_kind_name_plural(self.kind)
            title = '{} #{}'.format(title_start, self.pk)

            # works will be an array of Movies, Dance Pieces, etc.
            works = self.get_works()
            # We only need their titles:
            works = [str(w) for w in works]
            if len(works) > 0:
                if self.pk:
                    # (If it hasn't been saved it has no works yet.)
                    if len(works) == 1:
                        title = works[0]
                    elif len(works) > 1:
                        title = '{} and {}'.format(
                                        ', '.join(works[:-1]), works[-1])
            else:
                # It's like a Gig or Comedy; no works.
                roles = list(self.roles.all())
                if len(roles) == 1:
                    title = str(roles[0].creator.name)
                elif len(roles) == 0:
                    title = 'Event #{}'.format(self.pk)
                else:
                    roles = [r.creator.name for r in roles]
                    # Join with commas but 'and' for the last one:
                    title = '{} and {}'.format(
                                            ', '.join(roles[:-1]), roles[-1])
        else:
            title = self.title

        title = truncate_string(title, chars=255, at_word_boundary=True)

        return title

    def get_kinds():
        """
        Returns a list of the kind values ['gig', 'play', etc] in the order in
        which they're listed in `KIND_CHOICES`.
        """
        return [k for k,v in Event.KIND_CHOICES]

    def get_valid_kind_slugs():
        "Returns a list of the slugs that different kinds of Events can have."
        return list(Event.KIND_SLUGS.values())

    def get_kind_name_plural(kind):
        "e.g. 'Gigs' or 'Movies'."
        if kind == 'comedy':
            return 'Comedy'
        elif kind == 'dance':
            return 'Dance'
        else:
            return '{}s'.format(Event.get_kind_name(kind))

    def get_kind_name(kind):
        return {k:v for (k,v) in Event.KIND_CHOICES}[kind]

    def get_kinds_data():
        """
        Returns a dict of all the data about the kinds, keyed to the kind
        value. e.g:
            {
                'gig': {
                    'name': 'Gig',
                    'slug': 'gigs',
                    'name_plural': 'Gigs',
                },
                # etc
            }
        """
        kinds = {k:{'name':v} for k,v in Event.KIND_CHOICES}
        for k,data in kinds.items():
            kinds[k]['slug'] = Event.KIND_SLUGS[k]
            kinds[k]['name_plural'] = Event.get_kind_name_plural(k)
        return kinds

    def get_works(self):
        """
        Returns a list of the Event's Works (Movies, Dance Pieces, etc),
        in their correct orders.
        Or an empty list for Events that have none.

        NOTE: It only returns Works relevant to the Event's kind.
        e.g. A 'movie' Event will only return a list of any Movies in the
        Event, not any Plays. This reduces the number of database requests and
        we're assuming it's Good Enough.
        """
        # Want to get lists of each of the types of Work. But in the correct
        # order, so we need to get self.movie_selections.all() instead of
        # just self.movies.all(). The latter wouldn't use the MovieSelection
        # through model.

        if self.kind == 'concert':
            works = [s.work for s in self.classical_work_selections.all()]
        elif self.kind == 'dance':
            works = [s.work for s in self.dance_piece_selections.all()]
        elif self.kind == 'movie':
            works = [s.work for s in self.movie_selections.all()]
        elif self.kind == 'play':
            works = [s.work for s in self.play_selections.all()]
        else:
            works = []

        return works

    @property
    def kind_name(self):
        "e.g. 'Gig' or 'Movie'."
        return {k:v for (k,v) in self.KIND_CHOICES}[self.kind]

    @property
    def kind_name_plural(self):
        "e.g. 'Gigs' or 'Movies'."
        return Event.get_kind_name_plural(self.kind)

    @property
    def title_to_sort(self):
        """
        The string we use to create the title_sort property.
        We want to be able to sort by the event's Creators, if it doesn't
        have a title.
        """
        return self.make_title()


class Work(TimeStampedModelMixin, SluggedModelMixin, models.Model):
    """
    Abstract parent for things like DancePiece, Movie, Play, etc.
    Just so we stop duplicating common things.

    All children should also have a `creators` ManyToManyField to
    `spectator_core.Creator`.

    Example of getting a Works's creators:

        piece = DancePiece.objects.get(pk=1)

        # Just the creators:
        for creator in piece.creators.all():
            print(creator.name)

        # Include their roles:
        for role in piece.roles.all():
            print(role.dance_piece, role.creator, role.role_name)

        # When it's been seen:
        for ev in piece.event_set.all():
            print(ev.venue, ev.date)
    """
    title = models.CharField(null=False, blank=False, max_length=255)

    title_sort = NaturalSortField('title', max_length=255, default='',
            help_text="e.g. 'big piece, a' or 'biggest piece, the'.")

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        ordering = ('title_sort',)

    def get_list_url(self):
        "Handy in views. Override in child classes."
        raise NotImplementedError(
            "Child classes should return the list URL for this kind of Work.")


class ClassicalWork(Work):
    """
    A classical work itself, not an occasion on which it was watched.
    """
    creators = models.ManyToManyField('spectator_core.Creator',
                through='ClassicalWorkRole', related_name='classicalworks')

    class Meta:
        ordering = ('title_sort',)
        verbose_name = 'classical work'

    def get_absolute_url(self):
        return reverse('spectator:events:classicalwork_detail',
                                                    kwargs={'slug': self.slug})

    def get_list_url(self):
        return reverse('spectator:events:classicalwork_list')


class ClassicalWorkRole(BaseRole):
    """
    Through model for linking a Creator to a ClassicalWork, optionally via
    their role (e.g. 'Composer'.)
    """
    creator = models.ForeignKey('spectator_core.Creator',
                blank=False,
                on_delete=models.CASCADE, related_name='classical_work_roles')

    classical_work = models.ForeignKey('spectator_events.ClassicalWork',
                on_delete=models.CASCADE,
                related_name='roles')

    class Meta:
        ordering = ('role_order', 'role_name',)
        verbose_name = 'classical work role'


class ClassicalWorkSelection(models.Model):
    """
    Through model for linking a ClassicalWork to an Event with an order.
    """
    event = models.ForeignKey('spectator_events.Event',
                blank=False,
                on_delete=models.CASCADE,
                related_name='classical_work_selections')

    work = models.ForeignKey('spectator_events.ClassicalWork',
                blank=False,
                on_delete=models.CASCADE,
                related_name='events')

    order = models.PositiveSmallIntegerField(
                default=1,
                blank=False, null=False,
                help_text="Position on the Event programme." )

    class Meta:
        ordering = ('order',)
        verbose_name = 'classical work selection'

    def __str__(self):
        return '{}: {}'.format(self.event, self.work)


class DancePiece(Work):
    """
    A dance piece itself, not an occasion on which it was watched.
    """
    creators = models.ManyToManyField('spectator_core.Creator',
                        through='DancePieceRole', related_name='dancepieces')

    class Meta:
        ordering = ('title_sort',)
        verbose_name = 'dance piece'

    def get_absolute_url(self):
        return reverse('spectator:events:dancepiece_detail',
                                                    kwargs={'slug': self.slug})

    def get_list_url(self):
        return reverse('spectator:events:dancepiece_list')

class DancePieceRole(BaseRole):
    """
    Through model for linking a Creator to a DancePiece, optionally via their
    role (e.g. 'Choreographer'.)
    """
    creator = models.ForeignKey('spectator_core.Creator', blank=False,
                    on_delete=models.CASCADE, related_name='dance_piece_roles')

    dance_piece = models.ForeignKey('spectator_events.DancePiece',
                    on_delete=models.CASCADE, related_name='roles')

    class Meta:
        ordering = ('role_order', 'role_name',)
        verbose_name = 'dance piece role'


class DancePieceSelection(models.Model):
    """
    Through model for linking a DancePiece to an Event with an order.
    """
    event = models.ForeignKey('spectator_events.Event',
                blank=False,
                on_delete=models.CASCADE,
                related_name='dance_piece_selections')

    work = models.ForeignKey('spectator_events.DancePiece',
                blank=False,
                on_delete=models.CASCADE,
                related_name='events')

    order = models.PositiveSmallIntegerField(
                default=1,
                blank=False, null=False,
                help_text="Position on the Event programme." )

    class Meta:
        ordering = ('order',)
        verbose_name = 'dance piece selection'

    def __str__(self):
        return '{}: {}'.format(self.event, self.work)


class Movie(Work):
    """
    A movie itself, not an occasion on which it was watched.
    """
    YEAR_CHOICES = [(r,r) for r in range(1888, datetime.date.today().year+1)]
    YEAR_CHOICES.insert(0, ('', 'Select…'))

    creators = models.ManyToManyField('spectator_core.Creator',
                                    through='MovieRole', related_name='movies')

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

    def get_absolute_url(self):
        return reverse('spectator:events:movie_detail', kwargs={'slug':self.slug})

    def get_list_url(self):
        return reverse('spectator:events:movie_list')


class MovieRole(BaseRole):
    """
    Through model for linking a Creator to a Movie, optionally via their role
    (e.g.  'Director', 'Actor', etc.)
    """
    creator = models.ForeignKey('spectator_core.Creator', blank=False,
                        on_delete=models.CASCADE, related_name='movie_roles')

    movie = models.ForeignKey('spectator_events.Movie',
                        on_delete=models.CASCADE, related_name='roles')

    class Meta:
        ordering = ('role_order', 'role_name',)
        verbose_name = 'movie role'


class MovieSelection(models.Model):
    """
    Through model for linking a Movie to an Event with an order.
    """
    event = models.ForeignKey('spectator_events.Event',
                blank=False,
                on_delete=models.CASCADE,
                related_name='movie_selections')

    work = models.ForeignKey('spectator_events.Movie',
                blank=False,
                on_delete=models.CASCADE,
                related_name='events')

    order = models.PositiveSmallIntegerField(
                default=1,
                blank=False, null=False,
                help_text="Position on the Event programme." )

    class Meta:
        ordering = ('order',)
        verbose_name = 'movie selection'

    def __str__(self):
        return '{}: {}'.format(self.event, self.work)


class Play(Work):
    """
    A play itself, not an occasion on which it was watched.
    """
    creators = models.ManyToManyField('spectator_core.Creator',
                                    through='PlayRole', related_name='plays')

    def get_absolute_url(self):
        return reverse('spectator:events:play_detail',
                                                kwargs={'slug':self.slug})

    def get_list_url(self):
        return reverse('spectator:events:play_list')


class PlayRole(BaseRole):
    """
    Through model for linking a Creator to a Play, optionally via their role
    (e.g. 'Playwright'.)
    """
    creator = models.ForeignKey('spectator_core.Creator', blank=False,
                        on_delete=models.CASCADE, related_name='play_roles')

    play = models.ForeignKey('spectator_events.Play',
                        on_delete=models.CASCADE, related_name='roles')

    class Meta:
        ordering = ('role_order', 'role_name',)
        verbose_name = 'play role'


class PlaySelection(models.Model):
    """
    Through model for linking a Play to an Event with an order.
    """
    event = models.ForeignKey('spectator_events.Event',
                blank=False,
                on_delete=models.CASCADE,
                related_name='play_selections')

    work = models.ForeignKey('spectator_events.Play',
                blank=False,
                on_delete=models.CASCADE,
                related_name='events')

    order = models.PositiveSmallIntegerField(
                default=1,
                blank=False, null=False,
                help_text="Position on the Event programme." )

    class Meta:
        ordering = ('order',)
        verbose_name = 'play selection'

    def __str__(self):
        return '{}: {}'.format(self.event, self.work)


class Venue(TimeStampedModelMixin, SluggedModelMixin, models.Model):
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

    note = models.TextField(null=False, blank=True,
        help_text="Optional. Paragraphs will be surrounded with &lt;p&gt;&lt;/p&gt; tags. HTML allowed.")

    cinema_treasures_id = models.PositiveSmallIntegerField(
        null=True, blank=True,
        help_text='Optional. ID of a cinema at <a href="http://cinematreasures.org/">Cinema Treasures</a>.')

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
        return reverse('spectator:events:venue_detail', kwargs={'slug':self.slug})

    @property
    def country_name(self):
        if self.country:
            return self.COUNTRIES[self.country]
        else:
            return None

    @property
    def cinema_treasures_url(self):
        if self.cinema_treasures_id is not None:
            return 'http://cinematreasures.org/theaters/{}'.format(
                                                    self.cinema_treasures_id)
        else:
            return ''
