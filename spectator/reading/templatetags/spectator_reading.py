from collections import OrderedDict

from django import template
from django.db.models import Count, Q
from django.db.models.functions import TruncYear
from django.utils.html import format_html

from ..models import Publication, Reading


register = template.Library()


@register.simple_tag
def annual_reading_counts():
    """
    Returns a list of dicts, one per year of reading. In year order.
    Each dict is like:

        {'year':        datetime.date(2003, 1, 1),
         'book':        12,
         'periodical':  18,
         'total':       30,
         }

    We use the end_date of a Reading to count when that thing was read.
    """
    kinds = ['book', 'periodical']

    # This will have keys of years (strings) and dicts of data:
    # {
    #   '2003': {'books': 12, 'periodicals': 18},
    # }
    counts = OrderedDict()

    for kind in kinds:
        qs = Reading.objects.exclude(end_date__isnull=True) \
                            .filter(publication__kind=kind) \
                            .annotate(year=TruncYear('end_date')) \
                            .values('year') \
                            .annotate(count=Count('id')) \
                            .order_by('year')

        for year_data in qs:
            year_str = year_data['year'].strftime('%Y')
            if not year_str in counts:
                counts[year_str] = {
                    'year': year_data['year'],
                }

            counts[year_str][kind] = year_data['count']

    # Now translate counts into our final list, with totals, and 0s for kinds
    # when they have no Readings for that year.
    counts_list = []

    for year_str, data in counts.items():
        year_data = {
            'year': data['year'],
            'total': 0,
        }
        for kind in kinds:
            if kind in data:
                year_data[kind] = data[kind]
                year_data['total'] += data[kind]
            else:
                year_data[kind] = 0

        counts_list.append(year_data)

    return counts_list


@register.inclusion_tag('spectator_reading/includes/card_annual_reading_counts.html')
def annual_reading_counts_card(kind='all', current_year=None):
    """
    Displays years and the number of books/periodicals read per year.

    kind is one of 'book', 'periodical', 'all' (default).
    current_year is an optional date object representing the year we're already
        showing information about.
    """
    if kind == 'book':
        card_title = 'Books per year'
    elif kind == 'periodical':
        card_title = 'Periodicals per year'
    else:
        card_title = 'Reading per year'

    return {
            'card_title': card_title,
            'kind': kind,
            'years': annual_reading_counts(),
            'current_year': current_year
            }


@register.simple_tag
def in_progress_publications():
    """
    Returns a QuerySet of any Publications that are currently being read.
    """
    return Publication.in_progress_objects\
                        .select_related('series')\
                        .prefetch_related('roles__creator')\
                        .order_by('time_created')


@register.inclusion_tag('spectator_reading/includes/card_publications.html')
def in_progress_publications_card():
    """
    Displays Publications that are currently being read.
    """
    return {
            'card_title': 'Currently reading',
            'publication_list': in_progress_publications(),
            }


@register.simple_tag
def day_publications(date):
    """
    Returns a QuerySet of Publications that were being read on `date`.
    `date` is a date tobject.
    """
    readings = Reading.objects \
                        .filter(start_date__lte=date) \
                        .filter(
                            Q(end_date__gte=date)
                            |
                            Q(end_date__isnull=True)
                        )
    if readings:
        return Publication.objects.filter(reading__in=readings) \
                        .select_related('series') \
                        .prefetch_related('roles__creator')
    else:
        return Publication.objects.none()


@register.inclusion_tag('spectator_reading/includes/card_publications.html')
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


@register.simple_tag
def reading_years():
    """
    Returns a QuerySet of date objects, one for each year in which there are
    Readings.
    """
    return Reading.objects.dates('end_date', 'year')


@register.inclusion_tag('spectator_reading/includes/card_years.html')
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
