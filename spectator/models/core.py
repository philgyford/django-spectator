from django.db import models
try:
    # Django >= 1.10
    from django.urls import reverse
except ImportError:
    # Django < 1.10
    from django.core.urlresolvers import reverse

from ..utils import make_sort_name


class TimeStampedModelMixin(models.Model):
    "Should be mixed in to all models."
    time_created = models.DateTimeField(auto_now_add=True,
                help_text="The time this item was created in the database.")
    time_modified = models.DateTimeField(auto_now=True,
                help_text="The time this item was last saved to the database.")

    class Meta:
        abstract = True


class BaseRole(TimeStampedModelMixin, models.Model):
    """
    Base class for linking a Creator to a Book, Concert, MovieEvent, etc.

    Child classes should add fields like:

        creator = models.ForeignKey('Creator', blank=False,
                    on_delete=models.CASCADE, related_name='publication_roles')

        book = models.ForeignKey('Book', on_delete=models.CASCADE,
                                                        related_name='roles')
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


class Creator(TimeStampedModelMixin, models.Model):
    """
    A person or a group/company/organisation that is responsible for making all
    or part of a book, play, movie, gig, etc.

    Get the things they've worked on:

        creator = Creator.objects.get(pk=1)

        # Just Publication titles:
        for publication in creator.publications.all():
            print(publication.title)

        # Or Publications including the Creator and their role:
        for role in creator.publication_roles.all():
            print(role.publication, role.creator, role.role_name)

        # Similarly for Concerts:
        for role in creator.concert_roles.all():
            print(role.concert, role.creator, role.role_name)

        # And for Movies:
        for role in creator.movie_roles.all():
            print(role.movie, role.creator, role.role_name)

        # And for Plays:
        for role in creator.play_roles.all():
            print(role.play, role.creator, role.role_name)

        # And for PlaysProductions:
        for role in creator.play_production_roles.all():
            print(role.production, role.production.play, role.creator, role.role_name)
    """

    KIND_CHOICES = (
        ('individual', 'Individual'),
        ('group', 'Group'),
    )

    name = models.CharField(max_length=255,
            help_text="e.g. 'Douglas Adams' or 'The Long Blondes'.")

    sort_name = models.CharField(blank=True, max_length=255,
            help_text="e.g. 'Adams, Douglas' or 'Long Blondes, The'. If left blank, will be created automatically on save.")

    kind = models.CharField(max_length=20, choices=KIND_CHOICES,
                                                        default='individual')

    def save(self, *args, **kwargs):
        if self.sort_name == '':
            self.sort_name = self._make_sort_name(self.name, self.kind)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('sort_name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('spectator:creator_detail', kwargs={'pk':self.pk})

    def _make_sort_name(self, name, kind):
        if kind == 'group':
            return make_sort_name(name, 'thing')
        else:
            return make_sort_name(name, 'person')

