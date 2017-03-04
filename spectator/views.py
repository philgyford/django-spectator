from django.views.generic import DetailView, ListView, YearArchiveView,\
        TemplateView

from .models import Creator, Publication, PublicationSeries, Reading


class HomeView(TemplateView):
    template_name = 'spectator/home.html'


class CreatorListView(ListView):
    model = Creator


class CreatorDetailView(DetailView):
    model = Creator


class ReadingHomeView(ListView):
    model = Publication
    template_name = 'spectator/reading_home.html'


class PublicationSeriesListView(ListView):
    model = PublicationSeries


class PublicationSeriesDetailView(DetailView):
    model = PublicationSeries


class PublicationListView(ListView):
    model = Publication


class PublicationDetailView(DetailView):
    model = Publication


class ReadingYearArchiveView(YearArchiveView):
    date_field = 'end_date'
    model = Reading
