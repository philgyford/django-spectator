from django.views.generic import ListView

from ..models import Event


class EventsHomeView(ListView):
    model = Event
    template_name = 'spectator/events_home.html'

