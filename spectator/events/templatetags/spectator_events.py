from django import template

from ..models import Event


register = template.Library()


@register.assignment_tag
def recent_events(num=10):
    """
    Returns a QuerySet of Events that happened recently.
    `num` is the number returned.
    """
    return Event.objects.select_related('venue').order_by('-date')[:num]


@register.inclusion_tag('spectator/events/includes/card_events.html')
def recent_events_card(num=10):
    """
    Displays Events that happened recently.
    `num` is the number returned.
    """
    return {
            'card_title': 'Recent events',
            'event_list': recent_events(num=num),
            }

@register.assignment_tag
def day_events(date):
    """
    Returns a QuerySet of Events that happened on the supplied date.
    `date` is a date object.
    """
    return Event.objects.filter(date=date).select_related('venue')


@register.inclusion_tag('spectator/events/includes/card_events.html')
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


@register.assignment_tag
def events_years():
    """
    Returns a QuerySet of date objects, one for each year in which there are
    Events.
    """
    return Event.objects.dates('date', 'year')


@register.inclusion_tag('spectator/events/includes/card_years.html')
def events_years_card(current_year=None):
    return {
            'current_year': current_year,
            'years': events_years(),
            }


