from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from spectator.core.fields import NaturalSortField
from spectator.core.models import (
    BaseRole,
    SluggedModelMixin,
    ThumbnailModelMixin,
    TimeStampedModelMixin,
    thumbnail_upload_path,
)

from . import managers


def publication_upload_path(instance, filename):
    """
    This function is now only kept so that older migrations still work.

    No longer needed since moving the Publication.thumbnail field to the
    ThumbnailModelMixin.
    2020-04-07
    """
    return thumbnail_upload_path(instance, filename)


class PublicationSeries(TimeStampedModelMixin, SluggedModelMixin, models.Model):
    """
    A way to group `Publication`s into series.

    Get its Publications:

        series.publication_set.all()
    """

    title = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        help_text="e.g. 'The London Review of Books'.",
    )

    title_sort = NaturalSortField(
        "title",
        max_length=255,
        default="",
        help_text="e.g. 'london review of books, the'.",
    )

    url = models.URLField(
        null=False,
        blank=True,
        max_length=255,
        verbose_name="URL",
        help_text="e.g. 'https://www.lrb.co.uk/'.",
    )

    class Meta:
        ordering = ("title_sort",)
        verbose_name = "Publication series"
        verbose_name_plural = "Publication series"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "spectator:reading:publicationseries_detail", kwargs={"slug": self.slug}
        )


class PublicationRole(BaseRole):
    """
    Linking a creator to a Publication, optionally via their role (e.g.
    'Author', 'Editor', etc.)
    """

    creator = models.ForeignKey(
        "spectator_core.Creator",
        blank=False,
        on_delete=models.CASCADE,
        related_name="publication_roles",
    )

    publication = models.ForeignKey(
        "spectator_reading.Publication", on_delete=models.CASCADE, related_name="roles"
    )

    class Meta:
        ordering = ("role_order", "role_name")
        verbose_name = "Publication role"


class Publication(ThumbnailModelMixin, TimeStampedModelMixin, SluggedModelMixin):
    """
    Get a Publication's creators:

        publication = Publication.objects.get(pk=1)

        # Just the creators:
        for creator in publication.creators.all():
            print(creator.name)

        # Include their roles:
        for role in publication.roles.all():
            print(role.publication, role.creator, role.role_name)

    Get its readings:

        for reading in publication.reading_set.all():
            print(reading.start_date, reading.end_date)
    """

    class Kind(models.TextChoices):
        BOOK = "book", "Book"
        PERIODICAL = "periodical", "Periodical"

    title = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        help_text="e.g. 'Aurora' or 'Vol. 39 No. 4, 16 February 2017'.",
    )

    title_sort = NaturalSortField(
        "title",
        max_length=255,
        default="",
        help_text="e.g. 'clockwork orange, a' or 'world cities, the'.",
    )

    series = models.ForeignKey(
        "spectator_reading.PublicationSeries",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.BOOK)

    official_url = models.URLField(
        null=False,
        blank=True,
        max_length=255,
        verbose_name="Official URL",
        help_text="Official URL for this book/issue.",
    )

    isbn_uk = models.CharField(
        null=False,
        blank=True,
        max_length=20,
        verbose_name="UK ISBN",
        help_text="e.g. '0356500489'.",
    )

    isbn_us = models.CharField(
        null=False,
        blank=True,
        max_length=20,
        verbose_name="US ISBN",
        help_text="e.g. '0316098094'.",
    )

    notes_url = models.URLField(
        null=False,
        blank=True,
        max_length=255,
        verbose_name="Notes URL",
        help_text="URL of your notes/review.",
    )

    creators = models.ManyToManyField(
        "spectator_core.Creator", through="PublicationRole", related_name="publications"
    )

    # Managers

    objects = models.Manager()

    # Publications that are currently being read:
    in_progress_objects = managers.InProgressPublicationsManager()

    # Publications that haven't been started (have no Readings):
    unread_objects = managers.UnreadPublicationsManager()

    class Meta:
        ordering = ("title_sort",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "spectator:reading:publication_detail", kwargs={"slug": self.slug}
        )

    def get_current_reading(self):
        try:
            return self.reading_set.filter(end_date__isnull=True)[0]
        except IndexError:
            pass

    @property
    def amazon_uk_url(self):
        url = ""
        if self.isbn_uk:
            url = f"https://www.amazon.co.uk/gp/product/{self.isbn_uk}/"
            if (
                hasattr(settings, "SPECTATOR_AMAZON")
                and "uk" in settings.SPECTATOR_AMAZON
            ):
                url = "{}?tag={}".format(url, settings.SPECTATOR_AMAZON["uk"])
        return url

    @property
    def amazon_us_url(self):
        url = ""
        if self.isbn_us:
            url = f"https://www.amazon.com/dp/{self.isbn_us}/"
            if (
                hasattr(settings, "SPECTATOR_AMAZON")
                and "us" in settings.SPECTATOR_AMAZON
            ):
                url = "{}?tag={}".format(url, settings.SPECTATOR_AMAZON["us"])
        return url

    @property
    def amazon_urls(self):
        urls = []
        if self.isbn_uk:
            urls.append(
                {"url": self.amazon_uk_url, "name": "Amazon.co.uk", "country": "UK"}
            )
        if self.isbn_us:
            urls.append(
                {"url": self.amazon_us_url, "name": "Amazon.com", "country": "USA"}
            )
        return urls

    @property
    def has_urls(self):
        "Handy for templates."
        if self.isbn_uk or self.isbn_us or self.official_url or self.notes_url:  # noqa: SIM103
            return True
        else:
            return False


class Reading(TimeStampedModelMixin, models.Model):
    """
    A period when a Publication was read.
    """

    class DateGranularity(models.IntegerChoices):
        # Via https://www.flickr.com/services/api/misc.dates.html
        # SECOND = 0, "Y-m-d H:i:s"
        DAY = 3, "Y-m-d"
        MONTH = 4, "Y-m"
        YEAR = 6, "Y"
        # CIRCA = 8, "Circa..."

    publication = models.ForeignKey(
        "spectator_reading.Publication",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    start_date = models.DateField(null=True, blank=True)
    start_granularity = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        default=DateGranularity.DAY,
        choices=DateGranularity.choices,
    )
    end_date = models.DateField(null=True, blank=True)
    end_granularity = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        default=DateGranularity.DAY,
        choices=DateGranularity.choices,
    )
    is_finished = models.BooleanField(
        default=False, help_text="Did you finish the publication?"
    )

    objects = managers.EndDateAscendingReadingsManager()
    objects_desc = managers.EndDateDescendingReadingsManager()

    def __str__(self):
        return f"{self.publication} ({self.start_date} to {self.end_date})"

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            msg = "A Reading's end date can't be before its start date."
            raise ValidationError(msg)
