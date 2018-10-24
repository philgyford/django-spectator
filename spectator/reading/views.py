from django.db.models import Min
from django.http import Http404
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, ListView, YearArchiveView
from django.views.generic.detail import SingleObjectMixin

from spectator.core.models import Creator
from spectator.core.views import PaginatedListView
from .models import Publication, PublicationSeries, Reading


class ReadingHomeView(ListView):
    model = Publication
    template_name = 'spectator_reading/home.html'
    queryset = Publication.unread_objects.select_related('series')\
                            .prefetch_related('roles__creator').all()
    ordering = ['time_created',]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['in_progress_publication_list'] = \
                                            Publication.in_progress_objects\
                                            .select_related('series')\
                                            .prefetch_related('roles__creator')\
                                            .all()
        return context


class PublicationSeriesListView(ListView):
    model = PublicationSeries


class PublicationSeriesDetailView(SingleObjectMixin, PaginatedListView):
    template_name = 'spectator_reading/publicationseries_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=PublicationSeries.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publicationseries'] = self.object
        context['publication_list'] = context['object_list']
        return context

    def get_queryset(self):
        return self.object.publication_set.select_related('series')\
                            .prefetch_related('roles__creator').all()


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
        qs = super().get_queryset()
        qs = qs.filter(kind=self.publication_kind)\
                .select_related('series')\
                .prefetch_related('roles__creator')
        return qs

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
    # Could be set to 'periodical' or 'book' in get():
    publication_kind = None
    # Will be a QS of all publications finished this year:
    all_publications_queryset = None

    def get(self, request, *args, **kwargs):
        # Are we should 'book's (default) or 'periodical's?
        kind = self.kwargs.get('kind', None)
        if kind == 'periodicals':
            self.publication_kind = 'periodical'
        elif kind == 'books':
            self.publication_kind = 'book'
        elif kind is not None:
            raise Http404("'{}' is not a valid publication kind".format(kind))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publication_kind'] = self.publication_kind

        context['publication_count'] = self.all_publications_queryset.count()
        context['book_count'] = self.all_publications_queryset \
                                .filter(publication__kind='book').count()
        context['periodical_count'] = self.all_publications_queryset \
                                .filter(publication__kind='periodical').count()
        return context

    def get_queryset(self):
        "Reduce the number of queries and speed things up."
        qs = super().get_queryset()

        qs = qs.select_related('publication__series') \
                .prefetch_related('publication__roles__creator')

        return qs

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

        # Save the QuerySet for ALL kinds for use in get_context_data():
        self.all_publications_queryset = qs

        # Now filter the results if necessary:
        if self.publication_kind is not None:
            qs = qs.filter(publication__kind=self.publication_kind)

        return items, qs, info
