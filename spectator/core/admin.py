from django.contrib import admin

from .models import Creator


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_sort', 'kind',)
    list_filter = ('kind', )
    search_fields = ('name', 'name_sort', )

    fieldsets = (
        (None, {
            'fields': ('name', 'name_sort', 'slug', 'kind',)
        }),
        ('Times', {
            'classes': ('collapse',),
            'fields': ('time_created', 'time_modified',)
        }),
    )

    radio_fields = {'kind': admin.HORIZONTAL}
    readonly_fields = ('slug', 'name_sort', 'time_created', 'time_modified',)

