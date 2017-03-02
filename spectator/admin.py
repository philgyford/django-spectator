from django.contrib import admin

from .models import Book, BookRole, BookSeries, Concert, ConcertRole, Creator,\
        Reading, Venue


class ReadingInline(admin.TabularInline):
    model = Reading
    fields = ('book', 'start_date', 'end_date', 'is_finished',
                        'start_granularity', 'end_granularity',)
    raw_id_fields = ('book',)
    extra = 1


class BookRoleInline(admin.TabularInline):
    model = BookRole
    fields = ( 'creator', 'role_name', 'role_order',)
    raw_id_fields = ('creator',)
    extra = 1


class ConcertRoleInline(admin.TabularInline):
    model = ConcertRole
    fields = ( 'creator', 'role_name', 'role_order',)
    raw_id_fields = ('creator',)
    extra = 1


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ('sort_name', 'kind',)
    list_filter = ('kind', )
    search_fields = ('name', 'sort_name',)

    fieldsets = (
        (None, {
            'fields': ('name', 'sort_name', 'kind',)
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('time_created', 'time_modified',)


@admin.register(BookSeries)
class BookSeriesAdmin(admin.ModelAdmin):
    list_display = ('title', )

    fieldsets = (
        (None, {
            'fields': ('title', 'url', )
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('time_created', 'time_modified',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'kind', 'show_creators', 'series', )
    list_filter = ('kind', 'series', )
    search_fields = ('title',)

    fieldsets = (
        (None, {
            'fields': ( 'title', 'kind', 'series',
                        'isbn_gb', 'isbn_us',
                        'official_url', 'notes_url', )
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('time_created', 'time_modified',)

    inlines = [ BookRoleInline, ReadingInline, ]

    def show_creators(self, instance):
        names = [ str(r.creator) for r in instance.book_roles.all() ]
        if names:
            return ', '.join(names)
        else:
            return '-'
    # show_creators.allow_tags = True
    show_creators.short_description = 'Creators'


@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
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
