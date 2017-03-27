from django import template
from django.db.models import Q
from django.http import QueryDict
from django.utils.html import format_html

from ..models import Event, Publication, Reading


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
    return {
            'card_title': 'Currently reading',
            'publication_list': in_progress_publications(),
            }


@register.assignment_tag
def recent_events(num=10):
    """
    Returns a QuerySet of Events that happened recently.
    `num` is the number returned.
    """
    return Event.objects.select_related('venue').order_by('-date')[:num]


@register.inclusion_tag('spectator/events/includes/card_events.html')
def recent_events_card(num=10):
    return {
            'card_title': 'Recent events',
            'event_list': recent_events(num=num),
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


@register.assignment_tag
def day_events(date):
    """
    Returns a QuerySet of Events that happened on the supplied date.
    `date` is a date object.
    """
    return Event.objects.filter(date=date).select_related('venue')


@register.assignment_tag
def reading_years():
    """
    Returns a QuerySet of date objects, one for each year in which there are
    Readings.
    """
    return Reading.objects.dates('end_date', 'year')


@register.inclusion_tag('spectator/reading/includes/card_years.html')
def reading_years_card(current_year=None):
    return {
            'current_year': current_year,
            'years': reading_years(),
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


@register.simple_tag(takes_context=True)
def current_url_name(context):
    """
    Returns the name of the current URL, namespaced, or False.

    Example usage:

        {% current_url_name as url_name %}

        <a href="#"{% if url_name == 'myapp:home' %} class="active"{% endif %}">Home</a>

    """
    url_name = False
    if context.request.resolver_match:
        url_name = "{}:{}".format(
                                context.request.resolver_match.namespace,
                                context.request.resolver_match.url_name
                            )
    return url_name


@register.simple_tag(takes_context=True)
def query_string(context, key, value):
    """
    For adding/replacing a key=value pair to the GET string for a URL.

    eg, if we're viewing ?p=3 and we do {% url_replace order 'taken' %}
    then this returns "p=3&order=taken"

    And, if we're viewing ?p=3&order=uploaded and we do the same thing, we get
    the same result (ie, the existing "order=uploaded" is replaced).

    Expects the request object in context to do the above; otherwise it will
    just return a query string with the supplied key=value pair.
    """
    try:
        request = context['request']
        args = request.GET.copy()
    except KeyError:
        args = QueryDict('').copy()
    args[key] = value
    return args.urlencode()


@register.simple_tag
def reading_dates(reading):
    """
    Given a Reading, with start and end dates and granularities[1] it returns
    an HTML string representing that period. eg:

        * '1–6 Feb 2017'
        * '1 Feb to 3 Mar 2017'
        * 'Feb 2017 to Mar 2018'
        * '2017-2018'
    etc.

    [1] https://www.flickr.com/services/api/misc.dates.html
    """

    # 3 Sep 2017
    full_format = '<time datetime="%Y-%m-%d">%-d&nbsp;%b&nbsp;%Y</time>'
    # Sep 2017
    month_year_format = '<time datetime="%Y-%m">%b&nbsp;%Y</time>'
    # 2017
    year_format = '<time datetime="%Y">%Y</time>'
    # 3
    day_format = '<time datetime="%Y-%m-%d">%-d</time>'
    # 3 Sep
    day_month_format = '<time datetime="%Y-%m-%d">%-d&nbsp;%b</time>'
    # Sep
    month_format = '<time datetime="%Y-%m">%b</time>'

    # For brevity:
    start_date = reading.start_date
    end_date = reading.end_date
    start_gran = reading.start_granularity
    end_gran = reading.end_granularity

    # Are start and end in the same day, year or month?
    same_day = False
    same_month = False
    same_year = False

    if start_date and end_date:
        if start_date.strftime('%Y') == end_date.strftime('%Y'):
            same_year = True
            if start_date.strftime('%m%Y') == end_date.strftime('%m%Y'):
                same_month = True
                if start_date.strftime('%d%m%Y') == end_date.strftime('%d%m%Y'):
                    same_day = True

    start_str = ''
    end_str = ''
    output = ''

    # Make some basic start and end strings, which we might use...

    if start_date:
        if start_gran == 3:
            start_str = start_date.strftime(full_format)
        elif start_gran == 4:
            start_str = start_date.strftime(month_year_format)
        else:
            start_str = start_date.strftime(year_format)

    if end_date:
        if end_gran == 3:
            end_str = end_date.strftime(full_format)
        elif end_gran == 4:
            end_str = end_date.strftime(month_year_format)
        else:
            end_str = end_date.strftime(year_format)

    # Now make the final strings we'll return:

    if start_date and end_date:

        # A default which will be overridden in many cases. This covers:
        # 1 February 2017 to 3 March 2018
        # 1 February 2017 to March 2018
        # 1 February 2017 to 2018
        # February 2017 to 3 March 2018
        # February 2017 to March 2018
        # February 2017 to 2018
        # 2017 to 3 March 2018
        # 2017 to March 2018
        # 2017 to 2018
        output = '{} to {}'.format(start_str, end_str)

        if (start_gran == 4 or end_gran == 4) and same_month:
            # Only have enough to output 'February 2017'.
            output = start_str

        elif (start_gran == 6 or end_gran == 6) and same_year:
            # Only have enough to output '2017'.
            output = start_str

        elif start_gran == 3:
            if end_gran == 3:
                if same_day:
                    # 1 February 2017
                    output = start_str

                elif same_month:
                    # 1–6 February 2017
                    output = '{}–{}'.format(
                                        start_date.strftime(day_format),
                                        end_str)
                elif same_year:
                    # 1 February to 3 March 2017
                    output = '{} to {}'.format(
                                        start_date.strftime(day_month_format),
                                        end_str)
            elif end_gran == 4:
                if same_year:
                    # 1 February to March 2017
                    output = '{} to {}'.format(
                                        start_date.strftime(day_month_format),
                                        end_str)
        elif start_gran == 4:
            if end_gran == 3:
                if same_year:
                    # February to 3 March 2017
                    output = '{} to {}'.format(
                                            start_date.strftime(month_format),
                                            end_str)
            elif end_gran == 4:
                if same_year:
                    # February to March 2017
                    output = '{} to {}'.format(
                                            start_date.strftime(month_format),
                                            end_str)
    elif end_date:
        # Only an end_date.
        if end_gran == 3:
            # Finished on 1 February 2017
            output = "Finished on {}".format(end_str)
        else:
            # Finished in February 2017
            # Finished in 2017
            output = "Finished in {}".format(end_str)

    else:
        # No end_date: the reading has started, but not ended.
        if start_gran == 3:
            # Started on 1 February 2017
            output = "Started on {}".format(start_str)

        else:
            # Started in February 2017
            # Started in 2017
            output = "Started in {}".format(start_str)

    return format_html(output)
