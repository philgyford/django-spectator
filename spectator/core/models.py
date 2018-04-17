from django.db import models
from django.urls import reverse

from hashids import Hashids

from . import app_settings
from .fields import NaturalSortField
from .managers import CreatorManager


class TimeStampedModelMixin(models.Model):
    "Should be mixed in to all models."
    time_created = models.DateTimeField(auto_now_add=True,
                help_text="The time this item was created in the database.")
    time_modified = models.DateTimeField(auto_now=True,
                help_text="The time this item was last saved to the database.")

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
            kwargs['force_insert'] = False
            self.save(*args, **kwargs)

    def _generate_slug(self, value):
        """
        Generates a slug using a Hashid of `value`.
        """
        alphabet = app_settings.SLUG_ALPHABET
        salt = app_settings.SLUG_SALT

        hashids = Hashids(alphabet=alphabet, salt=salt, min_length=5)

        return hashids.encode(value)


class BaseRole(TimeStampedModelMixin, models.Model):
    """
    Base class for linking a Creator to a Book, Event, Movie, etc.

    Child classes should add fields like:

        creator = models.ForeignKey('spectator_core.Creator', blank=False,
                    on_delete=models.CASCADE, related_name='publication_roles')

        publication = models.ForeignKey('spectator_reading.Publication',
                    on_delete=models.CASCADE, related_name='roles')
    """
    role_name = models.CharField(null=False, blank=True, max_length=50,
            help_text="e.g. 'Headliner', 'Support', 'Editor', 'Illustrator', 'Director', etc. Optional.")

    role_order = models.PositiveSmallIntegerField(null=False, blank=False,
            default=1,
            help_text="The order in which the Creators will be listed.")

    class Meta:
        abstract = True
        ordering = ('role_order', 'role_name',)

    def __str__(self):
        if self.role_name:
            return '{} ({})'.format(self.creator, self.role_name)
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
        ('individual', 'Individual'),
        ('group', 'Group'),
    )

    name = models.CharField(max_length=255,
            help_text="e.g. 'Douglas Adams' or 'The Long Blondes'.")

    name_sort = NaturalSortField(
        'name', max_length=255, default='',
        help_text="Best for sorting groups. e.g. 'long blondes, the' or 'adams, douglas'.")

    kind = models.CharField(max_length=20, choices=KIND_CHOICES,
                                                        default='individual')

    objects = CreatorManager()

    class Meta:
        ordering = ('name_sort',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('spectator:creators:creator_detail',
                                                    kwargs={'slug':self.slug})

    @property
    def sort_as(self):
        "Used by the NaturalSortField."
        if self.kind == 'individual':
            return 'person'
        else:
            return 'thing'

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
        return self.works.filter(kind='classicalwork').distinct()

    def get_dance_pieces(self):
        return self.works.filter(kind='dancepiece').distinct()

    def get_exhibitions(self):
        return self.works.filter(kind='exhibition').distinct()

    def get_movies(self):
        return self.works.filter(kind='movie').distinct()

    def get_plays(self):
        return self.works.filter(kind='play').distinct()
