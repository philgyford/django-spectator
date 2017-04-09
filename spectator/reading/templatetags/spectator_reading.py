from django import template
from django.db.models import Q

from ..models import Publication, Reading

register = template.Library()


@register.assignment_tag
def in_progress_publications():
    """
    Returns a QuerySet of any Publications that are currently being read.
    """
    return Publication.in_progress_objects\
                        .select_related('series')\
                        .prefetch_related('roles__creator')\
                        .order_by('time_created')


@register.inclusion_tag('spectator/reading/includes/card_publications.html')
def in_progress_publications_card():
    """
    Displays Publications that are currently being read.
    """
    return {
            'card_title': 'Currently reading',
            'publication_list': in_progress_publications(),
            }


@register.assignment_tag
def day_publications(date):
    """
    Returns a QuerySet of Publications that were being read on `date`.
    `date` is a date tobject.
    """
    return Publication.objects\
                        .filter(reading__start_date__lte=date)\
                        .filter(
                            Q(reading__end_date__gte=date)
                            |
                            Q(reading__end_date__isnull=True)
                        )\
                        .select_related('series')\
                        .prefetch_related('roles__creator')


@register.inclusion_tag('spectator/reading/includes/card_publications.html')
def day_publications_card(date):
    """
    Displays Publications that were being read on `date`.
    `date` is a date tobject.
    """
    card_title = 'Reading on {}'.format(date.strftime('%-d %b %Y'))
    return {
            'card_title': card_title,
            'publication_list': day_publications(date=date),
            }


@register.assignment_tag
def reading_years():
    """
    Returns a QuerySet of date objects, one for each year in which there are
    Readings.
    """
    return Reading.objects.dates('end_date', 'year')


@register.inclusion_tag('spectator/reading/includes/card_years.html')
def reading_years_card(current_year=None):
    """
    Displays the years in which there are Readings.
    Each one is linked to the year archive page.
    current_year is a date object; this year won't be linked.
    """
    return {
            'current_year': current_year,
            'years': reading_years(),
            }


