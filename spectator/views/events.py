from django.views.generic import ListView

from ..models import Concert, Event, Movie, MovieEvent, Play,\
        PlayProductionEvent


class EventsListView(ListView):
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


class EventsHomeView(EventsListView):
    pass

class ConcertListView(EventsListView):
    model = Concert

class MovieEventListView(EventsListView):
    model = MovieEvent

class PlayProductionEventListView(EventsListView):
    model = PlayProductionEvent


class MovieListView(ListView):
    model = Movie

class PlayListView(ListView):
    model = Play

