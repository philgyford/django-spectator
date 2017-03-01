from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Creator, Book, BookSeries, Reading, Role


class ReadingInline(admin.TabularInline):
    model = Reading

    fieldsets = (
        (None, {
            'fields': ( 'book', 'start_date', 'end_date', 'is_finished',
                        'start_granularity', 'end_granularity',)
        }),
    )

    raw_id_fields = ('book',)
    extra = 1


class RoleInline(GenericTabularInline):
    model = Role

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

    inlines = [ RoleInline, ReadingInline, ]

    def show_creators(self, instance):
        names = [ str(r.creator) for r in instance.roles.all() ]
        if names:
            return ', '.join(names)
        else:
            return '-'
    # show_creators.allow_tags = True
    show_creators.short_description = 'Creators'


# @admin.register(Reading)
# class ReadingAdmin(admin.ModelAdmin):
    # list_display = ('book', 'start_date', 'end_date', 'is_finished',)
    # list_filter = ('end_date',)

    # fieldsets = (
        # (None, {
            # 'fields': ( 'book', 'start_date', 'end_date', 'is_finished',
                        # 'start_granularity', 'end_granularity',)
        # }),
        # ('Times', {
            # 'classes': ('collapse',),
            # 'fields': ('time_created', 'time_modified',)
        # }),
    # )

    # raw_id_fields = ('book',)
    # readonly_fields = ('time_created', 'time_modified',)

