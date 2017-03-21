from django.views.generic import DetailView, ListView

from . import PaginatedListView
from ..models import Concert, Event, Movie, MovieEvent, Play,\
        PlayProductionEvent


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
        return context

    def get_event_kind(self):
        return self.model.event_kind


class EventsHomeView(EventListView):
    pass

class ConcertEventListView(EventListView):
    model = Concert

class MovieEventListView(EventListView):
    model = MovieEvent

class PlayProductionEventListView(EventListView):
    model = PlayProductionEvent


class ConcertListView(ListView):
    model = Concert
    ordering = ['title_sort']

class MovieListView(ListView):
    model = Movie
    ordering = ['title_sort']

class PlayListView(ListView):
    model = Play
    ordering = ['title_sort']


class ConcertDetailView(DetailView):
    model = Concert

class MovieDetailView(DetailView):
    model = Movie

class PlayDetailView(DetailView):
    model = Play

