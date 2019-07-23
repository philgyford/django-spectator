from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Publication, PublicationRole, PublicationSeries, Reading


class ReadingInline(admin.TabularInline):
    model = Reading
    fields = (
        "publication",
        "start_date",
        "end_date",
        "is_finished",
        "start_granularity",
        "end_granularity",
    )
    raw_id_fields = ("publication",)
    extra = 1


class PublicationRoleInline(admin.TabularInline):
    model = PublicationRole
    fields = ("creator", "role_name", "role_order")
    raw_id_fields = ("creator",)
    extra = 1


@admin.register(PublicationSeries)
class PublicationSeriesAdmin(admin.ModelAdmin):
    list_display = ("title",)

    fieldsets = (
        (None, {"fields": ("title", "title_sort", "slug", "url")}),
        (
            "Times",
            {"classes": ("collapse",), "fields": ("time_created", "time_modified")},
        ),
    )

    readonly_fields = ("title_sort", "slug", "time_created", "time_modified")


class ReadingsListFilter(admin.SimpleListFilter):
    """
    Add filters for publications to list 'Unread' and 'In-progress' publications.
    """

    title = "reading"
    parameter_name = "readings"

    def lookups(self, request, model_admin):
        return (("in-progress", ("In progress")), ("unread", ("Unread")))

    def queryset(self, request, queryset):
        if self.value() == "in-progress":
            return queryset.filter(
                reading__start_date__isnull=False, reading__end_date__isnull=True
            )

        if self.value() == "unread":
            return queryset.filter(reading__isnull=True)


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "show_thumb", "kind", "show_creators", "series")
    list_filter = (ReadingsListFilter, "kind", "series")
    search_fields = ("title",)
    list_select_related = ("series",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "title_sort",
                    "show_thumb",
                    "cover",
                    "slug",
                    "kind",
                    "series",
                    "isbn_uk",
                    "isbn_us",
                    "official_url",
                    "notes_url",
                )
            },
        ),
        (
            "Times",
            {"classes": ("collapse",), "fields": ("time_created", "time_modified")},
        ),
    )

    radio_fields = {"kind": admin.HORIZONTAL}
    readonly_fields = (
        "title_sort",
        "show_thumb",
        "slug",
        "time_created",
        "time_modified",
    )

    inlines = [PublicationRoleInline, ReadingInline]

    def show_creators(self, instance):
        names = [str(r.creator) for r in instance.roles.all()]
        if names:
            return ", ".join(names)
        else:
            return "-"

    show_creators.short_description = "Creators"

    def show_thumb(self, instance):
        if instance.cover_thumbnail:
            return mark_safe(
                '<img src="%s" width="%s" height="%s" alt="Cover thumbnail">'
                % (
                    instance.cover_thumbnail.url,
                    round(instance.cover_thumbnail.width / 2),
                    round(instance.cover_thumbnail.height / 2),
                )
            )
        else:
            return None

    show_thumb.short_description = "Thumbnail"
