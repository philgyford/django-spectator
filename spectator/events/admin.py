from django.conf import settings
from django.contrib import admin
from django.core import urlresolvers
from django.core.exceptions import ValidationError
from django import forms

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
            'fields': ( 'kind', 'date', 'venue', 'title', 'title_sort', 'slug',)
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
    list_display = ('title', 'year', 'show_creators',)
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


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'country',)
    list_filter = ('country',)
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

