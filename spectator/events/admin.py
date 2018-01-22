from django import forms
from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.templatetags.l10n import unlocalize

from .models import Event, EventRole, ClassicalWork, ClassicalWorkRole,\
        DancePiece, DancePieceRole, Movie, MovieRole, Play, PlayRole, Venue


# INLINES.

class RoleInline(admin.TabularInline):
    "Parent class for the other *RoleInlines."
    fields = ( 'creator', 'role_name', 'role_order',)
    raw_id_fields = ('creator',)
    extra = 1

class EventRoleInline(RoleInline):
    model = EventRole

class ClassicalWorkRoleInline(RoleInline):
    model = ClassicalWorkRole

class DancePieceRoleInline(RoleInline):
    model = DancePieceRole

class MovieRoleInline(RoleInline):
    model = MovieRole

class PlayRoleInline(RoleInline):
    model = PlayRole


# MODEL ADMINS.

class EventAdminForm(forms.ModelForm):
    """
    Adding validation to ensure that plays, movies, classical works and dance
    pieces are added only when the Event's kind is appropriate.
    """
    class Meta:
        model = Event
        fields = '__all__'

    def clean_classicalworks(self):
        works = self.cleaned_data['classicalworks']
        num_works = len(works)

        if self.cleaned_data['kind'] == 'concert':
            if num_works == 0:
                raise ValidationError('If kind is "Classical concert" the '
                            'event should have at least one classical work.')
        elif num_works > 0:
            raise ValidationError('Only events of kind "Classical concert" '
                                    'should have related classical works.')
        return works

    def clean_dancepieces(self):
        pieces = self.cleaned_data['dancepieces']
        num_pieces = len(pieces)

        if self.cleaned_data['kind'] == 'dance':
            if num_pieces == 0:
                raise ValidationError('If kind is "Dance" the event should '
                                            'have at least one dance piece.')
        elif num_pieces > 0:
            raise ValidationError('Only events of kind "Dance" should have '
                                                    'related dance piece.')
        return pieces

    def clean_movie(self):
        movie = self.cleaned_data['movie']
        if self.cleaned_data['kind'] == 'movie':
            if movie is None:
                raise ValidationError(
                'If kind is "Movie" the event should have a related movie.')
        elif movie is not None:
            raise ValidationError(
                'Only events of kind "Movie" should have a related movie.')
        return movie

    def clean_play(self):
        play = self.cleaned_data['play']
        if self.cleaned_data['kind'] == 'play':
            if play is None:
                raise ValidationError(
                'If kind is "Play" the event should have a related play.')
        elif play is not None:
            raise ValidationError(
                'Only events of kind "Play" should have a related play.')
        return play


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm

    list_display = ('__str__', 'date', 'kind_name', 'venue',)
    list_filter = ('kind', 'date',)
    search_fields = ('title',)

    fieldsets = (
        (None, {
            'fields': ( 'kind', 'date', 'venue', 'title', 'title_sort', 'slug',
                        'note',)
        }),
        ('Things seen', {
            'fields': ('movie', 'play', 'classicalworks', 'dancepieces',)
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    filter_horizontal = ('classicalworks', 'dancepieces',)
    raw_id_fields = ('movie', 'play', 'venue',)
    readonly_fields = ('title_sort', 'slug', 'time_created', 'time_modified',)

    inlines = [EventRoleInline, ]

    class Media:
        js = (
            'js/admin/event.js',
        )


class ProductionAdmin(admin.ModelAdmin):
    """
    A parent class for MovieAdmin and PlayAdmin.
    """
    list_display = ('title', 'show_creators')
    search_fields = ('title',)

    readonly_fields = ('title_sort', 'time_created', 'time_modified',)

    def show_creators(self, instance):
        names = [ str(r.creator) for r in instance.roles.all() ]
        if len(names) == 0:
            return '-'
        elif len(names) <= 3:
            return ', '.join(names)
        else:
            # Too many to list them all.
            return '{} et al.'.format(names[0])
    show_creators.short_description = 'Creators'


@admin.register(ClassicalWork)
class ClassicalWorkAdmin(ProductionAdmin):
    fieldsets = (
        (None, {
            'fields': ( 'title', 'title_sort', 'slug',)
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('title_sort', 'slug', 'time_created', 'time_modified',)
    inlines = [ ClassicalWorkRoleInline, ]


@admin.register(DancePiece)
class DancePieceAdmin(ProductionAdmin):
    fieldsets = (
        (None, {
            'fields': ( 'title', 'title_sort',  'slug',)
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('title_sort', 'slug', 'time_created', 'time_modified',)
    inlines = [ DancePieceRoleInline, ]


@admin.register(Movie)
class MovieAdmin(ProductionAdmin):
    list_display = ('title', 'tidy_year', 'show_creators',)
    list_filter = ('year',)

    fieldsets = (
        (None, {
            'fields': ( 'title', 'title_sort', 'slug', 'year', 'imdb_id',)
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('title_sort', 'slug', 'time_created', 'time_modified',)
    inlines = [ MovieRoleInline, ]

    def tidy_year(self, obj):
        "Stop the year appearing like '2,018' when USE_THOUSAND_SEPARATOR=True"
        return unlocalize(obj.year)



@admin.register(Play)
class PlayAdmin(ProductionAdmin):
    fieldsets = (
        (None, {
            'fields': ( 'title', 'title_sort', 'slug',)
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('title_sort', 'slug', 'time_created', 'time_modified',)
    inlines = [ PlayRoleInline, ]


class CountryListFilter(admin.SimpleListFilter):
    """
    For filtering Venues by country.

    Used so that we only list countries that have at least one Venue assigned
    to them.

    Otherwise we have a very long list of countries, most of which are unused.
    """
    title = 'Country'

    parameter_name = 'country'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples like:

            [
                ('AU', 'Australia'),
                ('GB', 'UK'),
                ('US', 'USA'),
            ]

        One for each country that has at least one Venue.
        Sorted by the label names.
        """
        list_of_countries = []

        # We don't need the country_count but we need to annotate them in order
        # to group the results.
        qs = Venue.objects.exclude(country='') \
                            .values('country') \
                            .annotate(country_count=Count('country')) \
                            .order_by('country')
        for obj in qs:
            country = obj['country']
            list_of_countries.append(
                (country, Venue.COUNTRIES[country])
            )

        return sorted(list_of_countries, key=lambda c: c[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(country=self.value())
        else:
            return queryset


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'country',)
    list_filter = (CountryListFilter,)
    search_fields = ('name',)

    fieldsets = (
        (None, {
            'fields': ( 'name', 'name_sort', 'latitude', 'longitude',
                        'address', 'country',)
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('name_sort', 'time_created', 'time_modified',)

    class Media:
        if hasattr(settings, 'SPECTATOR_GOOGLE_MAPS_API_KEY') and settings.SPECTATOR_GOOGLE_MAPS_API_KEY:
            css = {
                'all': ('css/admin/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.SPECTATOR_GOOGLE_MAPS_API_KEY),
                'js/admin/location_picker.js',
            )
