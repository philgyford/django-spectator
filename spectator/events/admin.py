from django.conf import settings
from django.contrib import admin
from django.core import urlresolvers

from .models import Event, EventRole, Movie, MovieRole, Play, PlayRole, Venue


# INLINES.


class EventInline(admin.TabularInline):
    model = Event
    extra = 1


class EventRoleInline(admin.TabularInline):
    model = EventRole
    fields = ( 'creator', 'role_name', 'role_order',)
    raw_id_fields = ('creator',)
    extra = 1


class MovieRoleInline(admin.TabularInline):
    model = MovieRole
    fields = ( 'creator', 'role_name', 'role_order',)
    raw_id_fields = ('creator',)
    extra = 1


class PlayRoleInline(admin.TabularInline):
    model = PlayRole
    fields = ( 'creator', 'role_name', 'role_order',)
    raw_id_fields = ('creator',)
    extra = 1


# MODEL ADMINS.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    base_model = Event

    list_display = ('__str__', 'date', 'kind_name', 'venue',)
    list_filter = ('kind', 'date',)
    search_fields = ('title',)

    fieldsets = (
        (None, {
            'fields': ( 'kind', 'date', 'venue', 'title', 'title_sort',)
        }),
        ('Things seen', {
            'fields': ('movie', 'play',)
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    raw_id_fields = ('movie', 'play', 'venue',)
    readonly_fields = ('title_sort', 'time_created', 'time_modified',)

    inlines = [ EventRoleInline, ]


class ProductionAdmin(admin.ModelAdmin):
    """
    A parent class for MovieAdmin and PlayAdmin.
    """
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


@admin.register(Movie)
class MovieAdmin(ProductionAdmin):
    list_display = ('title', 'year', 'show_creators',)
    list_filter = ('year',)
    search_fields = ('title',)

    fieldsets = (
        (None, {
            'fields': ( 'title', 'title_sort', 'year', 'imdb_id',)
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('title_sort', 'time_created', 'time_modified',)

    inlines = [ MovieRoleInline, ]


@admin.register(Play)
class PlayAdmin(ProductionAdmin):
    list_display = ('title', 'show_creators')
    search_fields = ('title',)

    fieldsets = (
        (None, {
            'fields': ( 'title', 'title_sort', )
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('title_sort', 'time_created', 'time_modified',)

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

