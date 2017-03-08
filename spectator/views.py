from django.views.generic import DetailView, ListView, YearArchiveView,\
        TemplateView

from .models import Creator, Publication, PublicationSeries, Reading


class HomeView(TemplateView):
    template_name = 'spectator/home.html'


class CreatorListView(ListView):
    model = Creator
    creator_kind = 'individual'

    def get(self, request, *args, **kwargs):
        # Are we should 'individual's (default) or 'group's?
        if self.kwargs.get('kind', None) == 'group':
            self.creator_kind = 'group'
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creator_kind'] = self.creator_kind
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(kind=self.creator_kind)
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
    publication_kind = 'book'

    def get(self, request, *args, **kwargs):
        # Are we should 'book's (default) or 'periodical's?
        if self.kwargs.get('kind', None) == 'periodical':
            self.publication_kind = 'periodical'
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publication_kind'] = self.publication_kind
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(kind=self.publication_kind)
        return queryset


class PublicationDetailView(DetailView):
    model = Publication


class ReadingYearArchiveView(YearArchiveView):
    date_field = 'end_date'
    model = Reading
