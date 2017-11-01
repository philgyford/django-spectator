from django.contrib import admin

from .models import Publication, PublicationRole, PublicationSeries, Reading


class ReadingInline(admin.TabularInline):
    model = Reading
    fields = ('publication', 'start_date', 'end_date', 'is_finished',
                        'start_granularity', 'end_granularity',)
    raw_id_fields = ('publication',)
    extra = 1


class PublicationRoleInline(admin.TabularInline):
    model = PublicationRole
    fields = ( 'creator', 'role_name', 'role_order',)
    raw_id_fields = ('creator',)
    extra = 1


@admin.register(PublicationSeries)
class PublicationSeriesAdmin(admin.ModelAdmin):
    list_display = ('title',)

    fieldsets = (
        (None, {
            'fields': ('title', 'title_sort', 'slug', 'url', )
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('title_sort', 'slug', 'time_created', 'time_modified',)


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'kind', 'show_creators', 'series', )
    list_filter = ('kind', 'series', )
    search_fields = ('title',)
    list_select_related = ('series',)

    fieldsets = (
        (None, {
            'fields': ( 'title', 'title_sort', 'slug', 'kind', 'series',
                        'isbn_uk', 'isbn_us',
                        'official_url', 'notes_url', )
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    radio_fields = {'kind': admin.HORIZONTAL}
    readonly_fields = ('title_sort', 'slug', 'time_created', 'time_modified',)

    inlines = [ PublicationRoleInline, ReadingInline, ]

    def show_creators(self, instance):
        names = [ str(r.creator) for r in instance.roles.all() ]
        if names:
            return ', '.join(names)
        else:
            return '-'
    show_creators.short_description = 'Creators'


