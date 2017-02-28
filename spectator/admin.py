from django.contrib import admin

from .models import Creator


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ('sort_name', 'kind',)
    list_filter = ('kind', )

    fieldsets = (
        (None, {
            'fields': ('name', 'sort_name', 'kind',)
        }),
        ('Data', {
            'fields': ('time_created', 'time_modified',)
        }),
    )

    readonly_fields = ('time_created', 'time_modified',)

