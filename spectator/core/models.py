import os

from django.conf import settings
from django.db import models
from django.urls import reverse

from hashids import Hashids
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
import piexif

from . import app_settings
from .fields import NaturalSortField
from .managers import CreatorManager


class TimeStampedModelMixin(models.Model):
    "Should be mixed in to all models."
    time_created = models.DateTimeField(
        auto_now_add=True, help_text="The time this item was created in the database."
    )
    time_modified = models.DateTimeField(
        auto_now=True, help_text="The time this item was last saved to the database."
    )

    class Meta:
        abstract = True


class SluggedModelMixin(models.Model):
    """
    Adds a `slug` field which is generated from a Hashid of the model's pk.

    `slug` is generated on save, if it doesn't already exist.

    In theory we could use the Hashid'd slug in reverse to get the object's
    pk (e.g. in a view). But we're not relying on that, and simply using
    Hashid as a good method to generate unique, short URL-friendly slugs.
    """

    slug = models.SlugField(max_length=10, null=False, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = self._generate_slug(self.pk)
            # Don't want to insert again, if that's what was forced:
            kwargs["force_insert"] = False
            self.save(*args, **kwargs)

    def _generate_slug(self, value):
        """
        Generates a slug using a Hashid of `value`.
        """
        alphabet = app_settings.SLUG_ALPHABET
        salt = app_settings.SLUG_SALT

        hashids = Hashids(alphabet=alphabet, salt=salt, min_length=5)

        return hashids.encode(value)


def thumbnail_upload_path(instance, filename):
    """For ImageFields' upload_to attribute.
    e.g. '[MEDIA_ROOT]reading/publications/pok2d/my_cover_image.jpg'
    """
    # e.g. "publications" or "events":
    folder = "{}s".format(instance.__class__.__name__).lower()

    # This is kludgy, but...
    if folder == "publications":
        path = app_settings.READING_DIR_BASE
    elif folder == "events":
        path = app_settings.EVENTS_DIR_BASE
    else:
        raise NotImplementedError("No base directory set for this app's thumbnails")

    return os.path.join(path, folder, instance.slug, filename)


class ThumbnailModelMixin(models.Model):
    """
    Model mixin used to add a thumbnail ImageField, and associated
    fields in different sizes, powered by django-imagekit.

    * thumbnail - The uploaded image, stored in MEDIA
    * list_thumbnail - The smallest size, for lists of objects
    * list_thumbnail_2x - Retina version of list_thumbnail
    * detail_thumbnail - Used for detail pages
    * detail_thumbnail_2x - Retina version of detail_thumbnail

    Specify the dimensions using the THUMBNAIL_LIST_SIZE and
    THUMBNAIL_DETAIL_SIZE Django settings.
    """

    thumbnail = models.ImageField(
        upload_to=thumbnail_upload_path, null=False, blank=True, default=""
    )

    # Common ImageSpecField arguments:
    thumbnail_kwargs = {
        "source": "thumbnail",
        "format": "JPEG",
        "options": {"quality": 80},
    }

    # Calculate dimensions for 2x images:
    list_thumbnail_2x_dimensions = [d * 2 for d in app_settings.THUMBNAIL_LIST_SIZE]
    detail_thumbnail_2x_dimensions = [d * 2 for d in app_settings.THUMBNAIL_DETAIL_SIZE]

    list_thumbnail = ImageSpecField(
        processors=[ResizeToFit(*app_settings.THUMBNAIL_LIST_SIZE)], **thumbnail_kwargs
    )

    list_thumbnail_2x = ImageSpecField(
        processors=[ResizeToFit(*list_thumbnail_2x_dimensions)], **thumbnail_kwargs
    )

    detail_thumbnail = ImageSpecField(
        processors=[ResizeToFit(*app_settings.THUMBNAIL_DETAIL_SIZE)],
        **thumbnail_kwargs,
    )

    detail_thumbnail_2x = ImageSpecField(
        processors=[ResizeToFit(*detail_thumbnail_2x_dimensions)], **thumbnail_kwargs
    )

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # So we can see if it changed in save():
        self.__original_thumbnail = self.thumbnail

    def save(self, *args, **kwargs):
        """
        Move thumbnail file to correct location, and remove any location EXIF data.

        Ensure the uploaded thumbnail is in a directory for this object, with
        self.slug in the path.

        If adding a new object, e.g. in Admin's add screen, then the thumbnail
        is uploaded and saved BEFORE the object is saved. Saving the object gives
        it a pk, on which the slug is based. So the order needs to be:

        1. Save image to a path that won't have the slug in it
        2. Save the object, generating a pk and a slug
        3. Move image from its original location to a new directory in correct location.
        """
        super().save(*args, **kwargs)

        sep = os.path.sep

        if (
            self.thumbnail
            and f"{sep}{self.slug}{sep}" not in self.thumbnail.path
        ):
            # There's a new thumbnail but it's not in a directory with the slug name.
            # So we're going to move it, update the thumbnail property and then
            # re-save the model.
            # We have to do this AFTER the initial save, which generates the slug.
            self._move_uploaded_thumbnail()

            kwargs["force_insert"] = False
            super().save(*args, **kwargs)

        if self.thumbnail and self.thumbnail != self.__original_thumbnail:
            # Thumbnail has changed, so remove location data, if any.
            self.sanitize_thumbnail_exif_data()
            self.__original_thumbnail = self.thumbnail

    def sanitize_thumbnail_exif_data(self):
        """
        If the thumbnail has any GPS data in its EXIF data, remove it.
        """
        exif_dict = piexif.load(self.thumbnail.path)

        if "GPS" in exif_dict:
            del exif_dict["GPS"]
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, self.thumbnail.path)

    def _move_uploaded_thumbnail(self):
        """
        Move the thumbnail file from its original location, not in a slug directory,
        to a new slug-named directory. Then update the properties to point to the new
        location.
        """
        initial_path = self.thumbnail.path
        filename = os.path.basename(initial_path)

        new_name = thumbnail_upload_path(self, filename)
        new_path = os.path.join(settings.MEDIA_ROOT, new_name)

        if not os.path.exists(os.path.dirname(new_path)):
            os.makedirs(os.path.dirname(new_path))

        # Move the file:
        os.rename(initial_path, new_path)

        # Need to change both the field's name, and that for its
        # File object. Otherwise we get an error if we're using
        # django-imagekit's Optimistic cache strategy, trying to
        # generate the cache files on save.
        self.thumbnail.name = new_name
        self.thumbnail.file.name = new_path


class BaseRole(TimeStampedModelMixin, models.Model):
    """
    Base class for linking a Creator to a Book, Event, Movie, etc.

    Child classes should add fields like:

        creator = models.ForeignKey('spectator_core.Creator', blank=False,
                    on_delete=models.CASCADE, related_name='publication_roles')

        publication = models.ForeignKey('spectator_reading.Publication',
                    on_delete=models.CASCADE, related_name='roles')
    """

    role_name = models.CharField(
        null=False,
        blank=True,
        max_length=50,
        help_text="e.g. 'Headliner', 'Support', 'Editor', 'Illustrator', "
        "'Director', etc. Optional.",
    )

    role_order = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        default=1,
        help_text="The order in which the Creators will be listed.",
    )

    class Meta:
        abstract = True
        ordering = (
            "role_order",
            "role_name",
        )

    def __str__(self):
        if self.role_name:
            return "{} ({})".format(self.creator, self.role_name)
        else:
            return str(self.creator)


class Creator(TimeStampedModelMixin, SluggedModelMixin, models.Model):
    """
    A person or a group/company/organisation that is responsible for making all
    or part of a book, play, movie, gig, etc.

    Get the things they've worked on:

        creator = Creator.objects.get(pk=1)

        # Just Publication titles:
        for publication in creator.publications.distinct():
            print(publication.title)

        # You can do similar to that to get lists of `events`, `movies` and,
        # `plays` the Creator was involved with.


        # Or Publications including the Creator and their role:
        for role in creator.publication_roles.all():
            print(role.publication, role.creator, role.role_name)

        # Similarly for Event roles:
        for role in creator.event_roles.all():
            print(role.event, role.creator, role.role_name)

        # And for Work roles:
        for role in creator.work_roles.all():
            print(role.work, role.creator, role.role_name)
    """

    KIND_CHOICES = (
        ("individual", "Individual"),
        ("group", "Group"),
    )

    name = models.CharField(
        max_length=255, help_text="e.g. 'Douglas Adams' or 'The Long Blondes'."
    )

    name_sort = NaturalSortField(
        "name",
        max_length=255,
        default="",
        help_text="Best for sorting groups. e.g. 'long blondes, the' or "
        "'adams, douglas'.",
    )

    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default="individual")

    objects = CreatorManager()

    class Meta:
        ordering = ("name_sort",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("spectator:creators:creator_detail", kwargs={"slug": self.slug})

    @property
    def sort_as(self):
        "Used by the NaturalSortField."
        if self.kind == "individual":
            return "person"
        else:
            return "thing"

    def get_events(self):
        """
        All Events they're involved with, eliminating duplicates that occur
        with self.events.all() if they have multiple roles on the Event.
        """
        return self.events.distinct()

    def get_works(self):
        "All kinds of Work."
        return self.works.distinct()

    def get_classical_works(self):
        return self.works.filter(kind="classicalwork").distinct()

    def get_dance_pieces(self):
        return self.works.filter(kind="dancepiece").distinct()

    def get_exhibitions(self):
        return self.works.filter(kind="exhibition").distinct()

    def get_movies(self):
        return self.works.filter(kind="movie").distinct()

    def get_plays(self):
        return self.works.filter(kind="play").distinct()
