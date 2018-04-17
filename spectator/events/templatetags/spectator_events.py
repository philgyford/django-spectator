from django import template

from django.db.models import Count
from django.db.models.functions import TruncYear
from django.utils.html import format_html

from spectator.core.models import Creator
from spectator.core.utils import chartify
from spectator.core import app_settings
from ..models import Event, Work


register = template.Library()


@register.simple_tag
def annual_event_counts(kind='all'):
    """
    Returns a QuerySet of dicts, each one with these keys:

        * year - a date object representing the year
        * total - the number of events of `kind` that year

    kind - The Event `kind`, or 'all' for all kinds (default).
    """
    qs = Event.objects

    if kind != 'all':
        qs = qs.filter(kind=kind)

    qs = qs.annotate(year=TruncYear('date')) \
            .values('year') \
            .annotate(total=Count('id')) \
            .order_by('year')

    return qs


@register.inclusion_tag('spectator_events/includes/card_annual_event_counts.html')
def annual_event_counts_card(kind='all', current_year=None):
    """
    Displays years and the number of events per year.

    kind is an Event kind (like 'cinema', 'gig', etc.) or 'all' (default).
    current_year is an optional date object representing the year we're already
        showing information about.
    """
    if kind == 'all':
        card_title = 'Events per year'
    else:
        card_title = '{} per year'.format(Event.get_kind_name_plural(kind))

    return {
            'card_title': card_title,
            'kind': kind,
            'years': annual_event_counts(kind=kind),
            'current_year': current_year
            }


@register.simple_tag
def display_date(d):
    """
    Render a date/datetime (d) as a date, using the SPECTATOR_DATE_FORMAT
    setting. Wrap the output in a <time> tag.

    Time tags: http://www.brucelawson.co.uk/2012/best-of-time/
    """
    stamp = d.strftime('%Y-%m-%d')
    visible_date = d.strftime(app_settings.DATE_FORMAT)

    return format_html('<time datetime="%(stamp)s">%(visible)s</time>' % {
                'stamp': stamp,
                'visible': visible_date
            })


@register.inclusion_tag('spectator_events/includes/event_list_tabs.html')
def event_list_tabs(counts, current_kind, page_number=1):
    """
    Displays the tabs to different event_list pages.

    `counts` is a dict of number of events for each kind, like:
        {'all': 30, 'gig': 12, 'movie': 18,}

    `current_kind` is the event kind that's active, if any. e.g. 'gig',
        'movie', etc.

    `page_number` is the current page of this kind of events we're on.
    """
    return {
            'counts': counts,
            'current_kind': current_kind,
            'page_number': page_number,
            # A list of all the kinds we might show tabs for, like
            # ['gig', 'movie', 'play', ...]
            'event_kinds': Event.get_kinds(),
            # A dict of data about each kind, keyed by kind ('gig') including
            # data about 'name', 'name_plural' and 'slug':
            'event_kinds_data': Event.get_kinds_data(),
        }


@register.simple_tag
def recent_events(num=10):
    """
    Returns a QuerySet of Events that happened recently.
    `num` is the number returned.
    """
    return Event.objects.select_related('venue').order_by('-date')[:num]


@register.inclusion_tag('spectator_events/includes/card_events.html')
def recent_events_card(num=10):
    """
    Displays Events that happened recently.
    `num` is the number returned.
    """
    return {
            'card_title': 'Recent events',
            'event_list': recent_events(num=num),
            }

@register.simple_tag
def day_events(date):
    """
    Returns a QuerySet of Events that happened on the supplied date.
    `date` is a date object.
    """
    return Event.objects.filter(date=date).select_related('venue')


@register.inclusion_tag('spectator_events/includes/card_events.html')
def day_events_card(date):
    """
    Displays Events that happened on the supplied date.
    `date` is a date object.
    """
    d = date.strftime(app_settings.DATE_FORMAT)
    card_title = 'Events on {}'.format(d)
    return {
            'card_title': card_title,
            'event_list': day_events(date=date),
            }


@register.simple_tag
def events_years():
    """
    Returns a QuerySet of date objects, one for each year in which there are
    Events.
    """
    return Event.objects.dates('date', 'year')


@register.inclusion_tag('spectator_events/includes/card_years.html')
def events_years_card(current_year=None):
    """
    Displays a card showing all years in which we have Events, with a link to
    the archive pages.

    current_year is a date object representing the year we're displaying.
    """
    return {
            'current_year': current_year,
            'years': events_years(),
            }


@register.simple_tag
def most_seen_creators(event_kind=None, num=10):
    """
    Returns a QuerySet of the Creators that are associated with the most Events.
    """
    return Creator.objects.by_events(kind=event_kind)[:num]


@register.inclusion_tag('spectator_core/includes/card_chart.html')
def most_seen_creators_card(event_kind=None, num=10):
    """
    Displays a card showing the Creators that are associated with the most Events.
    """
    object_list = most_seen_creators(event_kind=event_kind, num=num)

    object_list = chartify(object_list, 'num_events', cutoff=1)

    return {
        'card_title': 'Most seen people/groups',
        'score_attr': 'num_events',
        'object_list': object_list,
    }


@register.simple_tag
def most_seen_creators_by_works(work_kind=None, role_name=None, num=10):
    """
    Returns a QuerySet of the Creators that are associated with the most Works.
    """
    return Creator.objects.by_works(kind=work_kind, role_name=role_name)[:num]


@register.inclusion_tag('spectator_core/includes/card_chart.html')
def most_seen_creators_by_works_card(work_kind=None, role_name=None, num=10):
    """
    Displays a card showing the Creators that are associated with the most Works.

    e.g.:

      {% most_seen_creators_by_works_card work_kind='movie' role_name='Director' num=5 %}
    """
    object_list = most_seen_creators_by_works(
                            work_kind=work_kind, role_name=role_name, num=num)

    object_list = chartify(object_list, 'num_works', cutoff=1)

    # Attempt to create a sensible card title...

    if role_name:
        # Yes, this pluralization is going to break at some point:
        creators_name = '{}s'.format(role_name.capitalize())
    else:
        creators_name = 'People/groups'

    if work_kind:
        works_name = Work.get_kind_name_plural(work_kind).lower()
    else:
        works_name = 'works'

    card_title = '{} with most {}'.format(creators_name, works_name)

    return {
        'card_title': card_title,
        'score_attr': 'num_works',
        'object_list': object_list,
    }


@register.simple_tag
def most_seen_works(kind=None, num=10):
    """
    Returns a QuerySet of the Works that are associated with the most Events.
    """
    return Work.objects.by_views(kind=kind)[:num]


@register.inclusion_tag('spectator_core/includes/card_chart.html')
def most_seen_works_card(kind=None, num=10):
    """
    Displays a card showing the Works that are associated with the most Events.
    """
    object_list = most_seen_works(kind=kind, num=num)

    object_list = chartify(object_list, 'num_views', cutoff=1)

    if kind:
        card_title = 'Most seen {}'.format(
                                    Work.get_kind_name_plural(kind).lower())
    else:
        card_title = 'Most seen works'

    return {
        'card_title': card_title,
        'score_attr': 'num_views',
        'object_list': object_list,
        'name_attr': 'title',
        'use_cite': True,
    }
