from django import template

from ..models import Event


register = template.Library()


@register.inclusion_tag('spectator_events/includes/event_list_tabs.html')
def event_list_tabs(counts, current_kind):
    """
    Displays the tabs to different event_list pages.

    `counts` is a dict of number of events for each kind, like:
        {'all': 30, 'gig': 12, 'movie': 18,}

    `current_kind` is the event kind that's active, if any. e.g. 'gig',
        'movie', etc.
    """
    return {
            'counts': counts,
            'current_kind': current_kind,
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
    card_title = 'Events on {}'.format(date.strftime('%-d %b %Y'))
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
