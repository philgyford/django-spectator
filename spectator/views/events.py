from django.conf import settings
from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectMixin

from . import PaginatedListView
from ..models import Concert, Event, Movie, MovieEvent, Play,\
        PlayProductionEvent, MiscEvent, Venue


class EventListView(PaginatedListView):
    """
    Parent class for any pages that list a type of Event.
    Includes context of counts of all different Event types,
    plus the kind of event this page is for,
    plus adding `event_list` (synonym for `object_list`).
    """
    model = Event
    ordering = ['-date',]
    template_name = 'spectator/event_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.add_counts_to_context_data(context)
        # The kind of event we're listing on this page:
        context['event_kind'] = self.get_event_kind()
        context['event_list'] = context['object_list']
        return context

    def add_counts_to_context_data(self, context):
        context['event_count'] = Event.objects.count()
        context['concert_count'] = Concert.objects.count()
        context['movieevent_count'] = MovieEvent.objects.count()
        context['playproductionevent_count'] = \
                                            PlayProductionEvent.objects.count()
        context['miscevent_count'] = MiscEvent.objects.count()
        return context

    def get_event_kind(self):
        return self.model.event_kind

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('venue')
        return qs


## EVENTs and its children.

class EventsHomeView(EventListView):
    pass


class ConcertEventListView(EventListView):
    model = Concert

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related('roles__creator')
        return qs


class MovieEventListView(EventListView):
    model = MovieEvent

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('movie')
        return qs


class PlayProductionEventListView(EventListView):
    model = PlayProductionEvent

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('production', 'production__play')
        return qs


class MiscEventVisitListView(EventListView):
    model = MiscEvent

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related('roles__creator')
        return qs


## Concert, Movie, Play, etc themselves; not the events.

class ConcertListView(PaginatedListView):
    model = Concert
    ordering = ['title_sort']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('venue').prefetch_related('roles__creator')
        return qs


class MovieListView(PaginatedListView):
    model = Movie
    ordering = ['title_sort']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related('roles__creator')
        return qs


class PlayListView(PaginatedListView):
    model = Play
    ordering = ['title_sort']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related('roles__creator')
        return qs


class MiscEventListView(PaginatedListView):
    model = MiscEvent
    ordering = ['title_sort']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related('roles__creator')
        return qs


# VENUEs

class VenueListView(PaginatedListView):
    model = Venue
    ordering = ['name_sort']


## DETAIL VIEWS

class ConcertDetailView(DetailView):
    model = Concert

class MovieDetailView(DetailView):
    model = Movie

class PlayDetailView(DetailView):
    model = Play

class MiscEventDetailView(DetailView):
    model = MiscEvent


class VenueDetailView(SingleObjectMixin, PaginatedListView):
    template_name = 'spectator/venue_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Venue.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['venue'] = self.object
        context['event_list'] = context['object_list']
        if hasattr(settings, 'SPECTATOR_GOOGLE_MAPS_API_KEY') and settings.SPECTATOR_GOOGLE_MAPS_API_KEY:
            if self.object.latitude is not None and self.object.longitude is not None:
                context['SPECTATOR_GOOGLE_MAPS_API_KEY'] = settings.SPECTATOR_GOOGLE_MAPS_API_KEY
        return context

    def get_queryset(self):
        return self.object.event_set.order_by('-date')

