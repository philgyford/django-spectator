from django.views.generic import DetailView, ListView, YearArchiveView,\
        TemplateView

from .models import Creator, Publication, PublicationSeries, Reading


class HomeView(TemplateView):
    template_name = 'spectator/home.html'


class CreatorListView(ListView):
    model = Creator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('kind', None) == 'group':
            context['creator_kind'] = 'group'
        else:
            context['creator_kind'] = 'individual'
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('kind', None) == 'group':
            queryset = queryset.filter(kind='group')
        else:
            queryset = queryset.filter(kind='individual')
        return queryset


class CreatorDetailView(DetailView):
    model = Creator


class ReadingHomeView(ListView):
    model = Publication
    template_name = 'spectator/reading_home.html'
    queryset = Publication.unread_objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['in_progress_publications'] = \
                                        Publication.in_progress_objects.all()
        return context


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
