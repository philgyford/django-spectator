from collections import OrderedDict

from django.db.models import Count
from django.db.models.functions import TruncYear

from .models import Reading


def annual_reading_counts(kind='all'):
    """
    Returns a list of dicts, one per year of reading. In year order.
    Each dict is like this (if kind is 'all'):

        {'year':        datetime.date(2003, 1, 1),
         'book':        12,    # only included if kind is 'all' or 'book'
         'periodical':  18,    # only included if kind is 'all' or 'periodical'
         'total':       30,    # only included if kind is 'all'
         }

    We use the end_date of a Reading to count when that thing was read.

    kind is one of 'book', 'periodical' or 'all', for both.
    """
    if kind == 'all':
        kinds = ['book', 'periodical']
    else:
        kinds = [kind]

    # This will have keys of years (strings) and dicts of data:
    # {
    #   '2003': {'books': 12, 'periodicals': 18},
    # }
    counts = OrderedDict()

    for k in kinds:
        qs = Reading.objects.exclude(end_date__isnull=True) \
                            .filter(publication__kind=k) \
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

            counts[year_str][k] = year_data['count']

    # Now translate counts into our final list, with totals, and 0s for kinds
    # when they have no Readings for that year.
    counts_list = []

    for year_str, data in counts.items():
        year_data = {
            'year': data['year'],
        }
        if kind == 'all':
            year_data['total'] = 0

        for k in kinds:
            if k in data:
                year_data[k] = data[k]
                if kind == 'all':
                    year_data['total'] += data[k]
            else:
                year_data[k] = 0

        counts_list.append(year_data)

    return counts_list
