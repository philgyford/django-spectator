from django.conf import settings
from django.contrib import admin

from polymorphic.admin import PolymorphicParentModelAdmin,\
    PolymorphicChildModelAdmin, PolymorphicChildModelFilter

from ..models import Concert, ConcertRole, Event,\
        Movie, MovieEvent, MovieRole,\
        Play, PlayProduction, PlayProductionEvent,\
        PlayProductionRole, PlayRole,\
        Venue


# INLINES.

class ConcertRoleInline(admin.TabularInline):
    model = ConcertRole
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


class PlayProductionRoleInline(admin.TabularInline):
    model = PlayProductionRole
    fields = ( 'creator', 'role_name', 'role_order',)
    raw_id_fields = ('creator',)
    extra = 1


# MODEL ADMINS.

@admin.register(Event)
class EventAdmin(PolymorphicParentModelAdmin):
    base_model = Event
    child_models = (Concert, MovieEvent, PlayProductionEvent)

    list_display = ('__str__', 'date', 'venue',)
    list_filter = (PolymorphicChildModelFilter, 'date',)
    # Get child models too, which means __str__ better reflects the child
    # model. But, makes for more queries.
    polymorphic_list = True


@admin.register(Concert)
class ConcertAdmin(PolymorphicChildModelAdmin):
    base_model = Concert
    show_in_index = False # Hide this model from the Admin index.

    list_display = ('__str__', 'date', 'venue',)
    list_filter = ('date',)
    search_fields = ('title',)

    fieldsets = (
        (None, {
            'fields': ( 'title', 'date', 'venue',)
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    raw_id_fields = ('venue',)
    readonly_fields = ('time_created', 'time_modified',)

    inlines = [ ConcertRoleInline, ]


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year')
    list_filter = ('year',)
    search_fields = ('title',)

    fieldsets = (
        (None, {
            'fields': ( 'title', 'year', 'imdb_id',)
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('time_created', 'time_modified',)

    inlines = [ MovieRoleInline, ]


@admin.register(MovieEvent)
class MovieEventAdmin(PolymorphicChildModelAdmin):
    base_model = MovieEvent
    show_in_index = False # Hide this model from the Admin index.

    list_display = ('movie', 'date', 'venue',)
    list_filter = ('date',)
    search_fields = ('movie__title',)

    fieldsets = (
        (None, {
            'fields': ( 'movie', 'date', 'venue',)
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    raw_id_fields = ('movie', 'venue',)
    readonly_fields = ('time_created', 'time_modified',)


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_creators')
    search_fields = ('title',)

    fieldsets = (
        (None, {
            'fields': ( 'title', )
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('time_created', 'time_modified',)

    inlines = [ PlayRoleInline, ]

    def show_creators(self, instance):
        names = [ str(r.creator) for r in instance.roles.all() ]
        if names:
            return ', '.join(names)
        else:
            return '-'
    show_creators.short_description = 'Creators'


@admin.register(PlayProduction)
class PlayProductionAdmin(admin.ModelAdmin):
    list_display = ('play', 'title', 'show_creators')
    search_fields = ('title',)

    fieldsets = (
        (None, {
            'fields': ( 'play', 'title', )
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    raw_id_fields = ('play',)
    readonly_fields = ('time_created', 'time_modified',)

    inlines = [ PlayProductionRoleInline, ]

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


@admin.register(PlayProductionEvent)
class PlayProductionEventAdmin(PolymorphicChildModelAdmin):
    base_model = PlayProductionEvent
    show_in_index = False # Hide this model from the Admin index.

    list_display = ('production', 'date', 'venue',)
    list_filter = ('date',)
    search_fields = ('production__title', 'production__play__title')

    fieldsets = (
        (None, {
            'fields': ( 'production', 'date', 'venue',)
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    raw_id_fields = ('production', 'venue',)
    readonly_fields = ('time_created', 'time_modified',)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    fieldsets = (
        (None, {
            'fields': ( 'name', 'latitude', 'longitude',)
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('time_created', 'time_modified',)

    class Media:
        if hasattr(settings, 'SPECTATOR_GOOGLE_MAPS_API_KEY') and settings.SPECTATOR_GOOGLE_MAPS_API_KEY:
            css = {
                'all': ('css/admin/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.SPECTATOR_GOOGLE_MAPS_API_KEY),
                'js/admin/jquery.location_picker.js',
            )

