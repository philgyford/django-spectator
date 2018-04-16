from django.db.models import Min
from django.http import Http404
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.views.generic import DetailView, ListView, YearArchiveView
from django.views.generic.detail import SingleObjectMixin

from spectator.core import app_settings
from spectator.core.models import Creator
from spectator.core.views import PaginatedListView
from .models import Event, Venue, Work


class EventListView(PaginatedListView):
    """
    Includes context of counts of all different Event types,
    plus the kind of event this page is for,
    plus adding `event_list` (synonym for `object_list`).

    Expects a `kind_slug` like 'movies', 'gigs', 'concerts', etc.
    """
    model = Event
    ordering = ['-date',]

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('kind_slug', None)
        if slug is not None and slug not in Event.get_valid_kind_slugs():
            raise Http404("Invalid kind_slug: '%s'" % slug)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update( self.get_event_counts() )

        # e.g. 'concert'
        kind = self.get_event_kind()
        context['event_kind'] = kind

        if kind:
            # e.g. 'Concert':
            context['event_kind_name'] = Event.get_kind_name(kind)
            # e.g. 'Concerts':
            context['event_kind_name_plural'] = Event.get_kind_name_plural(kind)

        context['event_list'] = context['object_list']

        return context

    def get_event_counts(self):
        """
        Returns a dict like:
            {'counts': {
                'all': 30,
                'movie': 12,
                'gig': 10,
            }}
        """
        counts = {'all': Event.objects.count(),}

        for k,v in Event.KIND_CHOICES:
            # e.g. 'movie_count':
            counts[k] = Event.objects.filter(kind=k).count()

        return {'counts': counts,}

    def get_event_kind(self):
        """
        Unless we're on the front page we'll have a kind_slug like 'movies'.
        We need to translate that into an event `kind` like 'movie'.
        """
        slug = self.kwargs.get('kind_slug', None)
        if slug is None:
            return None  # Front page; showing all Event kinds.
        else:
            slugs_to_kinds = {v:k for k,v in Event.KIND_SLUGS.items()}
            return slugs_to_kinds.get(slug, None)

    def get_queryset(self):
        "Restrict to a single kind of event, if any, and include Venue data."
        qs = super().get_queryset()

        kind = self.get_event_kind()
        if kind is not None:
            qs = qs.filter(kind=kind)

        qs = qs.select_related('venue')

        return qs


class EventDetailView(DetailView):
    model = Event


class EventYearArchiveView(YearArchiveView):
    allow_empty = True
    date_field = 'date'
    make_object_list = True
    model = Event
    ordering = 'date'

    def get_queryset(self):
        "Reduce the number of queries and speed things up."
        qs = super().get_queryset()
        qs = qs.select_related('venue')
        return qs

    def get_dated_items(self):
        items, qs, info = super().get_dated_items()

        if 'year' in info and info['year']:
            # Get the earliest date we have an Event for:
            date_min = Event.objects.aggregate(Min('date'))['date__min']
            # Make it a 'yyyy-01-01' date:
            min_year_date = date_min.replace(month=1, day=1)
            if info['year'] < min_year_date:
                # The year we're viewing is before our minimum date, so 404.
                raise Http404(_("No %(verbose_name_plural)s available") % {
                    'verbose_name_plural': force_text(qs.model._meta.verbose_name_plural)
                })
            elif info['year'] == min_year_date:
                # This is the earliest year we have events for, so
                # there is no previous year.
                info['previous_year'] = None

        return items, qs, info


# WORKS


class WorkMixin():
    kind_slug = None

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('kind_slug', None)
        if slug is not None and slug not in Work.get_valid_kind_slugs():
            raise Http404("Invalid kind_slug: '%s'" % slug)
        else:
            self.kind_slug = slug

        return super().get(request, *args, **kwargs)

    def get_work_kind(self):
        """
        We'll have a kind_slug like 'movies'.
        We need to translate that into a work `kind` like 'movie'.
        """
        slugs_to_kinds = {v:k for k,v in Work.KIND_SLUGS.items()}
        return slugs_to_kinds.get(self.kind_slug, None)


class WorkListView(WorkMixin, PaginatedListView):
    model = Work

    def get_queryset(self):
        kind = self.get_work_kind()
        qs = super().get_queryset()
        qs = qs.filter(kind=kind)
        qs = qs.prefetch_related('roles__creator')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 'movie', 'Movie', and 'Movies' respectively:
        kind = self.get_work_kind()
        kind_name = Work.get_kind_name(kind)
        kind_name_plural = Work.get_kind_name_plural(kind)

        context['page_title'] = kind_name_plural
        context['breadcrumb_list_title'] = kind_name_plural

        context['work_kind'] = kind
        context['work_kind_name'] = kind_name
        context['work_kind_name_plural'] = kind_name_plural

        context['breadcrumb_list_url'] = \
                        self.model().get_list_url(kind_slug=self.kind_slug)

        return context


class WorkDetailView(WorkMixin, DetailView):
    model = Work

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        kind = self.get_work_kind()

        context['breadcrumb_list_title'] = Work.get_kind_name_plural(kind)

        context['breadcrumb_list_url'] =  \
                        self.model().get_list_url(kind_slug=self.kind_slug)

        return context


# VENUES

class VenueListView(PaginatedListView):
    model = Venue
    ordering = ['name_sort']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['country_list'] = self.get_countries()

        return context

    def get_countries(self):
        """
        Returns a list of dicts, one per country that has at least one Venue
        in it.

        Each dict has 'code' and 'name' elements.
        The list is sorted by the country 'name's.
        """
        qs = Venue.objects.values('country') \
                                    .exclude(country='') \
                                    .distinct() \
                                    .order_by('country')

        countries = []

        for c in qs:
            countries.append({
                'code': c['country'],
                'name': Venue.get_country_name(c['country'])
            })

        return sorted(countries, key=lambda k: k['name'])


class VenueDetailView(SingleObjectMixin, PaginatedListView):
    template_name = 'spectator_events/venue_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Venue.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['venue'] = self.object

        context['event_list'] = context['object_list']

        if app_settings.GOOGLE_MAPS_API_KEY:
            if self.object.latitude is not None and self.object.longitude is not None:
                context['SPECTATOR_GOOGLE_MAPS_API_KEY'] = app_settings.GOOGLE_MAPS_API_KEY

        return context

    def get_queryset(self):
        return self.object.event_set.order_by('-date')
