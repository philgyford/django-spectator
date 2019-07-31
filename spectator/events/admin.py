from django.contrib import admin
from django.db.models import Count
from django.templatetags.l10n import unlocalize

from imagekit.admin import AdminThumbnail

from ..core import app_settings
from .models import Event, EventRole, Work, WorkRole, WorkSelection, Venue


# INLINES


class EventRoleInline(admin.TabularInline):
    model = EventRole
    fields = ("creator", "role_name", "role_order")
    raw_id_fields = ("creator",)
    extra = 0


class WorkRoleInline(admin.TabularInline):
    model = WorkRole
    fields = ("creator", "role_name", "role_order")
    raw_id_fields = ("creator",)
    extra = 0


class WorkSelectionInline(admin.TabularInline):
    model = WorkSelection
    fields = ("work", "order")
    raw_id_fields = ("work",)
    extra = 0


# MODEL ADMINS.


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = ("__str__", "date", "list_thumbnail", "kind_name", "venue")
    list_filter = ("kind", "date")
    search_fields = ("title",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "kind",
                    "date",
                    "venue",
                    "venue_name",
                    "title",
                    "title_sort",
                    "detail_thumbnail",
                    "ticket",
                    "slug",
                    "note",
                )
            },
        ),
        (
            "Times",
            {"classes": ("collapse",), "fields": ("time_created", "time_modified")},
        ),
    )

    raw_id_fields = ("venue",)
    readonly_fields = (
        "title_sort",
        "slug",
        "detail_thumbnail",
        "time_created",
        "time_modified",
    )

    inlines = [WorkSelectionInline, EventRoleInline]

    detail_thumbnail = AdminThumbnail(
        image_field="ticket", template="spectator_core/admin/detail_thumbnail.html"
    )

    list_thumbnail = AdminThumbnail(
        image_field="ticket", template="spectator_core/admin/list_thumbnail.html"
    )

    def save_related(self, request, form, formsets, change):
        """
        When the Admin saves the Event, the related M2M things, like Movies,
        haven't yet been saved. So when the Event's title_sort field has
        nothing to go on.

        So, cheekily, after the parent's save_related() method has saved
        all the M2M fields, we save the Event again. This time its
        title_sort will be set correctly.
        """
        super().save_related(request, form, formsets, change)
        form.instance.save()


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "tidy_year")
    search_fields = ("title",)
    list_filter = ("kind", "year")

    fieldsets = (
        (None, {"fields": ("kind", "title", "title_sort", "slug", "year", "imdb_id")}),
        (
            "Times",
            {"classes": ("collapse",), "fields": ("time_created", "time_modified")},
        ),
    )

    readonly_fields = ("title_sort", "slug", "time_created", "time_modified")
    inlines = [WorkRoleInline]

    def tidy_year(self, obj):
        "Stop the year appearing like '2,018' when USE_THOUSAND_SEPARATOR=True"
        if obj.year:
            return unlocalize(obj.year)
        else:
            return "-"

    tidy_year.short_description = "Year"


class CountryListFilter(admin.SimpleListFilter):
    """
    For filtering Venues by country.

    Used so that we only list countries that have at least one Venue assigned
    to them.

    Otherwise we have a very long list of countries, most of which are unused.
    """

    title = "Country"

    parameter_name = "country"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples like:

            [
                ('AU', 'Australia'),
                ('GB', 'UK'),
                ('US', 'USA'),
            ]

        One for each country that has at least one Venue.
        Sorted by the label names.
        """
        list_of_countries = []

        # We don't need the country_count but we need to annotate them in order
        # to group the results.
        qs = (
            Venue.objects.exclude(country="")
            .values("country")
            .annotate(country_count=Count("country"))
            .order_by("country")
        )
        for obj in qs:
            country = obj["country"]
            list_of_countries.append((country, Venue.COUNTRIES[country]))

        return sorted(list_of_countries, key=lambda c: c[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(country=self.value())
        else:
            return queryset


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "country")
    list_filter = (CountryListFilter,)
    search_fields = ("name",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "name_sort",
                    "note",
                    "cinema_treasures_id",
                    "latitude",
                    "longitude",
                    "address",
                    "country",
                )
            },
        ),
        (
            "Times",
            {"classes": ("collapse",), "fields": ("time_created", "time_modified")},
        ),
    )

    readonly_fields = ("name_sort", "time_created", "time_modified")

    class Media:
        if app_settings.GOOGLE_MAPS_API_KEY:
            css = {"all": ("css/admin/location_picker.css",)}
            js = (
                "https://maps.googleapis.com/maps/api/js?key={}".format(
                    app_settings.GOOGLE_MAPS_API_KEY
                ),
                "js/admin/location_picker.js",
            )
