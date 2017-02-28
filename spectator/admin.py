from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Creator, Book, BookSeries, Role


class RoleInline(GenericTabularInline):
    model = Role


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ('sort_name', 'kind',)
    list_filter = ('kind', )

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
    list_display = ('title', 'kind', 'series',)
    list_filter = ('kind', 'series', )

    fieldsets = (
        (None, {
            'fields': ('title', 'series',
                        'isbn_gb', 'isbn_us',
                        'official_url', 'notes_url', )
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('time_created', 'time_modified',)

    inlines = [
        RoleInline
    ]
