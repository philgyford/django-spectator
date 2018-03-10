from django.core.paginator import InvalidPage
from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, ListView, YearArchiveView,\
        TemplateView

from .apps import spectator_apps
from .models import Creator
from .paginator import DiggPaginator

if spectator_apps.is_enabled('events'):
    from spectator.events.models import Event

if spectator_apps.is_enabled('reading'):
    from spectator.reading.models import Publication


class PaginatedListView(ListView):
    """Use this instead of ListView to provide standardised pagination."""
    paginator_class = DiggPaginator
    paginate_by = 50
    page_kwarg = 'p'

    # See spectator.paginator for what these mean:
    paginator_body = 5
    paginator_margin = 2
    paginator_padding = 2
    paginator_tail = 2

    def __init__(self, **kwargs):
        return super().__init__(**kwargs)

    def paginate_queryset(self, queryset, page_size):
        """
        Paginate the queryset, if needed.

        This is EXACTLY the same as the standard ListView.paginate_queryset()
        except for this line:
            page = paginator.page(page_number, softlimit=True)
        Because we want to use the DiggPaginator's softlimit option.
        So that if you're viewing a page of, say, Flickr photos, and you switch
        from viewing by Uploaded Time to viewing by Taken Time, the new
        ordering might have fewer pages. In that case we want to see the final
        page, not a 404. The softlimit does that, but I can't see how to use
        it without copying all of this...
        """
        paginator = self.get_paginator(
            queryset,
            page_size,
            orphans = self.get_paginate_orphans(),
            allow_empty_first_page = self.get_allow_empty(),
            body    = self.paginator_body,
            margin  = self.paginator_margin,
            padding = self.paginator_padding,
            tail    = self.paginator_tail,
        )
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_("Page is not 'last', nor can it be converted to an int."))
        try:
            page = paginator.page(page_number, softlimit=False)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                'page_number': page_number,
                'message': str(e)
            })


class HomeView(TemplateView):
    template_name = 'spectator_core/home.html'

    # How many recent events to show:
    num_recent_events = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if spectator_apps.is_enabled('reading'):
            context.update( self.get_reading_context() )

        if spectator_apps.is_enabled('events'):
            context.update( self.get_events_context() )

        return context

    def get_events_context(self):
        context = {}

        context['recent_event_list'] = Event.objects\
                                        .select_related('venue')\
                                    .order_by('-date')[:self.num_recent_events]

        return context


    def get_reading_context(self):
        context = {}

        context['in_progress_publication_list'] = \
                                Publication.in_progress_objects\
                                .select_related('series')\
                                .prefetch_related('roles__creator').all()
        return context


class CreatorListView(PaginatedListView):
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
        context['individual_count'] = Creator.objects.filter(
                                                    kind='individual').count()
        context['group_count'] = Creator.objects.filter(
                                                    kind='group').count()

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(kind=self.creator_kind)
        return queryset


class CreatorDetailView(DetailView):
    model = Creator
