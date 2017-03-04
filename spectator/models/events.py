# coding: utf-8
import datetime

from django.db import models
from django.core.validators import RegexValidator

from polymorphic.models import PolymorphicModel

from . import BaseRole, Creator, TimeStampedModelMixin


class Event(TimeStampedModelMixin, PolymorphicModel):
    """
    Parent class for different kinds of event: Concert, MovieEvent, PlayEvent.

    A child class can add its own fields.
    """
    date = models.DateField(null=True, blank=False)
    venue = models.ForeignKey('Venue', blank=False)

    class Meta:
        ordering = ['date',]

    def __str__(self):
        return 'Event #{}'.format(self.pk)


class ConcertRole(BaseRole):
    """
    Through model for linking a creator to a Concert, optionally via their role
    (e.g. 'Headliner', 'Support', etc.)
    """
    creator = models.ForeignKey('Creator', blank=False,
                        on_delete=models.CASCADE, related_name='concert_roles')

    concert = models.ForeignKey('Concert', on_delete=models.CASCADE,
                                                        related_name='roles')


class Concert(Event):
    """
    A gig.

    Get a Concert's creators:

        concert = Concert.objects.get(pk=1)

        # Just the creators:
        for creator in concert.creators.all():
            print(creator.name)

        # Include their roles:
        for role in concert.roles.all():
            print(role.concert, role.creator, role.role_name)
    """
    title = models.CharField(null=False, blank=True, max_length=255,
            help_text="Optional. e.g., 'Indietracks 2017', 'Radio 1 Roadshow'.")

    creators = models.ManyToManyField(Creator, through='ConcertRole',
                                                    related_name='concerts')

    def __str__(self):
        if self.title:
            return self.title
        else:
            roles = list(self.roles.all())
            if len(roles) == 0:
                return 'Concert #{}'.format(self.pk)
            elif len(roles) == 1:
                return str(roles[0].creator.name)
            else:
                roles = [r.creator.name for r in roles]
                # Join with commas but 'and' for the last one:
                return '{} and {}'.format(
                            ', '.join(roles[:-1]),
                            roles[-1]
                        )


class MovieRole(BaseRole):
    """
    Through model for linking a creator to a Movie, optionally via their role
    (e.g.  'Director', 'Actor', etc.)
    """
    creator = models.ForeignKey('Creator', blank=False,
                        on_delete=models.CASCADE, related_name='movie_roles')

    movie = models.ForeignKey('Movie', on_delete=models.CASCADE,
                                                        related_name='roles')


class Movie(TimeStampedModelMixin, models.Model):
    """
    A movie itself, not an occasion on which it was watched.

    Get a Movie's creators:

        movie = Movie.objects.get(pk=1)

        # Just the creators:
        for creator in movie.creators.all():
            print(creator.name)

        # Include their roles:
        for role in movie.roles.all():
            print(role.movie, role.creator, role.role_name)
    """
    YEAR_CHOICES = [(r,r) for r in range(1888, datetime.date.today().year+1)]
    YEAR_CHOICES.insert(0, ('', 'Select…'))

    title = models.CharField(null=False, blank=False, max_length=255)
    creators = models.ManyToManyField(Creator, through='MovieRole',
                                                        related_name='movies')

    imdb_id = models.CharField(null=False, blank=True, max_length=12,
                    verbose_name='IMDb ID',
                    help_text="Starts with 'tt', e.g. 'tt0100842'.",
                    validators=[
                        RegexValidator(
                            regex='^tt\d{7,10}$',
                            message='IMDb ID should be like "tt1234567"',
                            code='invalid_imdb_id'
                        )
                    ]
                )

    year = models.PositiveSmallIntegerField(null=True, blank=True,
                default=None,
                help_text="Year of release.")

    class Meta:
        ordering = ('title',)

    def __str__(self):
        if self.year:
            return '{} ({})'.format(self.title, self.year)
        else:
            return self.title


class MovieEvent(Event):
    """
    An occasion on which a Movie was watched.
    """
    movie = models.ForeignKey('Movie', null=False, blank=False)

    def __str__(self):
        return str(self.movie)


class PlayRole(BaseRole):
    """
    Through model for linking a creator to a Play, optionally via their role
    (e.g. 'Author'.)
    """
    creator = models.ForeignKey('Creator', blank=False,
                        on_delete=models.CASCADE, related_name='play_roles')

    play = models.ForeignKey('Play', on_delete=models.CASCADE,
                                                        related_name='roles')


class Play(TimeStampedModelMixin, models.Model):
    """
    A play itself, not an occasion on which it was watched.

    Get a Play's creators:

        play = Play.objects.get(pk=1)

        # Just the creators:
        for creator in play.creators.all():
            print(creator.name)

        # Include their roles:
        for role in play.roles.all():
            print(role.play, role.creator, role.role_name)
    """
    title = models.CharField(null=False, blank=False, max_length=255)
    creators = models.ManyToManyField(Creator, through='PlayRole',
                                                        related_name='plays')

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class PlayProductionRole(BaseRole):
    """
    Through model for linking a creator to a particular production of a Play,
    optionally via their role (e.g. 'Director' or 'Actor'.)
    """
    creator = models.ForeignKey('Creator', blank=False,
                on_delete=models.CASCADE, related_name='play_production_roles')

    production = models.ForeignKey('PlayProduction', on_delete=models.CASCADE,
                                                related_name='roles')


class PlayProduction(TimeStampedModelMixin, models.Model):
    """
    A particular production of a play by a certain company/director/etc.

    Get a PlayProduction's creators:

        production = PlayProduction.objects.get(pk=1)

        # Just the creators:
        for creator in production.creators.all():
            print(creator.name)

        # Include their roles:
        for role in production.roles.all():
            print(role.production.play, role.production.title,\
                    role.creator, role.role_name)
    """
    play = models.ForeignKey('Play', null=False, blank=False)

    title = models.CharField(null=False, blank=True, max_length=255,
            help_text="Optional title of this production of the play.")

    creators = models.ManyToManyField('Creator', through='PlayProductionRole',
                    related_name='play_productions',
                    help_text="The director, actors, etc. in this production.")

    class Meta:
        ordering = ('play__title',)

    def __str__(self):
        if self.title:
            return self.title
        else:
            roles = list(self.roles.all())
            if len(roles) == 0:
                return 'Production of {}'.format(self.play)
            elif len(roles) == 1:
                return '{} by {}'.format(self.play, roles[0].creator)
            else:
                return '{} by {} et al.'.format(
                            self.play,
                            roles[0].creator.name
                        )


class PlayProductionEvent(Event):
    """
    An occasion on which a PlayProduction was watched.
    """
    production = models.ForeignKey('PlayProduction', blank=False)

    def __str__(self):
        return str(self.production)


class Venue(TimeStampedModelMixin, models.Model):
    """
    Where an event happens.
    """
    name = models.CharField(null=False, blank=False, max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,
                                                        null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,
                                                        null=True, blank=True)

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name

