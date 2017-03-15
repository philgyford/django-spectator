from django.db.models import Min
from django.http import Http404
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, ListView, YearArchiveView
from django.views.generic.detail import SingleObjectMixin

from . import PaginatedListView
from ..models import Publication, PublicationSeries, Reading


class ReadingHomeView(ListView):
    model = Publication
    template_name = 'spectator/reading_home.html'
    queryset = Publication.unread_objects.all()
    ordering = ['time_created',]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['in_progress_publication_list'] = \
                Publication.in_progress_objects.all().order_by('time_created')
        return context


class PublicationSeriesListView(ListView):
    model = PublicationSeries


class PublicationSeriesDetailView(SingleObjectMixin, PaginatedListView):
    template_name = "spectator/publicationseries_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=PublicationSeries.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publicationseries'] = self.object
        context['publication_list'] = context['object_list']
        return context

    def get_queryset(self):
        return self.object.publication_set.all()


class PublicationListView(PaginatedListView):
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
        context['book_count'] = Publication.objects.filter(kind='book').count()
        context['periodical_count'] = Publication.objects.filter(
                                                    kind='periodical').count()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(kind=self.publication_kind)
        return queryset

    def get_ordering(self):
        if self.publication_kind == 'periodical':
            return ('series__title_sort', 'title_sort',)
        else:
            return ('title_sort',)


class PublicationDetailView(DetailView):
    model = Publication


class ReadingYearArchiveView(YearArchiveView):
    allow_empty = True
    date_field = 'end_date'
    make_object_list = True
    model = Reading
    ordering = 'end_date'

    def get_dated_items(self):
        items, qs, info = super().get_dated_items()

        if 'year' in info and info['year']:
            # Get the earliest date we have a Reading for:
            end_date_min = Reading.objects.aggregate(
                                            Min('end_date'))['end_date__min']
            # Make it a 'yyyy-01-01' date:
            min_year_date = end_date_min.replace(month=1, day=1)
            if info['year'] < min_year_date:
                # The year we're viewing is before our minimum date, so 404.
                raise Http404(_("No %(verbose_name_plural)s available") % {
                    'verbose_name_plural': force_text(qs.model._meta.verbose_name_plural)
                })
            elif info['year'] == min_year_date:
                # This is the earliest year we have readings for, so
                # there is no previous year.
                info['previous_year'] = None

        return items, qs, info

