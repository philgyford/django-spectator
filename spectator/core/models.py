from django.db import models
try:
    # Django >= 1.10
    from django.urls import reverse
except ImportError:
    # Django < 1.10
    from django.core.urlresolvers import reverse

from .fields import NaturalSortField


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
        for publication in creator.publications.distinct():
            print(publication.title)

        # You can do similar to that to get lists of `concerts`, `movies`,
        # `plays` and `play_productions` the Creator was involved with.


        # Or Publications including the Creator and their role:
        for role in creator.publication_roles.all():
            print(role.publication, role.creator, role.role_name)

        # Similarly for Concert roles:
        for role in creator.concert_roles.all():
            print(role.concert, role.creator, role.role_name)

        # And for Movie roles:
        for role in creator.movie_roles.all():
            print(role.movie, role.creator, role.role_name)

        # And for Play roles:
        for role in creator.play_roles.all():
            print(role.play, role.creator, role.role_name)

        # And for PlaysProduction roles:
        for role in creator.play_production_roles.all():
            print(role.production, role.production.play, role.creator, role.role_name)
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

    class Meta:
        ordering = ('name_sort',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('spectator:creator_detail', kwargs={'pk':self.pk})

    @property
    def sort_as(self):
        "Used by the NaturalSortField."
        if self.kind == 'individual':
            return 'person'
        else:
            return 'thing'

    def get_movies(self):
        """
        A list of all the Movies the Creator worked on.
        Each one also has these properties:
        * `creator_roles` - QuerySet of MovieRole objects for this Creator.
        * `creator_role_names` - List of the role_names (if any this Creator
            had. Note, this could be empty if none of the roles have names.
        """
        movies = []
        for movie in self.movies.distinct():
            movie.creator_roles = movie.roles.filter(creator=self)
            movie.creator_role_names = []
            for role in movie.creator_roles:
                if role.role_name:
                    movie.creator_role_names.append(role.role_name)
            movies.append(movie)
        return movies

    def get_plays(self):
        """
        A list of all the Plays the Creator worked on.
        Each one also has these properties:
        * `creator_roles` - QuerySet of PlayRole objects for this Creator.
        * `creator_role_names` - List of the role_names (if any this Creator
            had. Note, this could be empty if none of the roles have names.
        """
        plays = []
        for play in self.plays.distinct():
            play.creator_roles = play.roles.filter(creator=self)
            play.creator_role_names = []
            for role in play.creator_roles:
                if role.role_name:
                    play.creator_role_names.append(role.role_name)
            plays.append(play)
        return plays

    def get_play_productions(self):
        """
        A list of all the PlayProductions the Creator worked on.
        Each one also has these properties:
        * `creator_roles` - QuerySet of PlayProductionRole objects for this
            Creator.
        * `creator_role_names` - List of the role_names (if any this Creator
            had. Note, this could be empty if none of the roles have names.
        """
        productions = []
        for production in self.play_productions.distinct():
            production.creator_roles = production.roles.filter(creator=self)
            production.creator_role_names = []
            for role in production.creator_roles:
                if role.role_name:
                    production.creator_role_names.append(role.role_name)
            productions.append(production)
        return productions

    def get_plays_and_productions(self):
        """
        Returns a list that combines Plays and PlayProductions, ordered by
        the Plays' `title_sort` field.

        It includes all Plays that the Creator had a role in, and all Plays
        which has PlayProductions in which the Creator had a role.

        Something like:

            [
                {
                    'play': Play1,
                    'productions': [ Production1, Production2, ],
                },
                {
                    'play': Play2,
                    'productions': [],
                },
            ]

        Here, the Creator was in two PlayProductions of Play1 (and may have
        had a role in creating Play1 itself). And also maybe wrote Play2 but
        didn't have a role in any PlayProductions of it.

        All Plays and PlayProductions have `creator_roles` and
        `creator_role_names` properties, as in `self.get_plays()` and
        `self.get_play_productions`.
        """
        plays = self.get_plays()
        # Make an initial dict, keyed by IDs of the plays:
        both = {p.id:{'play':p,'productions':[],} for p in plays}

        for production in self.get_play_productions():
            play_id = production.play_id
            if production.play_id in both:
                both[play_id]['productions'].append(production)
            else:
                both[play_id] = {
                    'play': production.play,
                    'productions': [ production, ]
                }

        both = list(both.values())
        both.sort(key=lambda x: x['play'].title_sort)

        return both

