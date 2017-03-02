# coding: utf-8
import datetime

from django.db import models
from django.core.validators import RegexValidator

from . import BaseRole, Creator, TimeStampedModelMixin


class BaseEvent(TimeStampedModelMixin, models.Model):
    """
    Parent class for different kinds of event: Concert, MovieEvent, PlayEvent.
    """
    title = models.CharField(null=False, blank=True, max_length=255,
            help_text="e.g., 'Indietracks 2017', 'Radio 1 Roadshow'.")
    date = models.DateField(null=True, blank=False)
    venue = models.ForeignKey('Venue', blank=False)

    class Meta:
        abstract = True
        ordering = ['date',]


class ConcertRole(BaseRole):
    """
    Linking a creator to a Concert, optionally via their role (e.g.
    'Headliner', 'Support', etc.)
    """
    creator = models.ForeignKey('Creator', blank=False,
                        on_delete=models.CASCADE, related_name='concert_roles')

    concert = models.ForeignKey('Concert', on_delete=models.CASCADE,
                                                        related_name='roles')


class Concert(BaseEvent):
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
    creators = models.ManyToManyField(Creator, through='ConcertRole',
                                                    related_name='concerts')

    def __str__(self):
        if self.title:
            return self.title
        else:
            creators = list(self.creators.all())
            if len(creators) == 0:
                return 'Concert <{}>'.format(self.pk)
            elif len(creators) == 1:
                return str(creators[0])
            else:
                creators = [str(c) for c in creators]
                # Join with commas but 'and' for the last one:
                return '{} and {}'.format(
                            ', '.join(creators[:-1]),
                            creators[-1]
                        )


class MovieRole(BaseRole):
    """
    Linking a creator to a Movie, optionally via their role (e.g.  'Director',
    'Actor', etc.)
    """
    creator = models.ForeignKey('Creator', blank=False,
                        on_delete=models.CASCADE, related_name='movie_roles')

    movie = models.ForeignKey('Movie', on_delete=models.CASCADE,
                                                        related_name='roles')


class Movie(TimeStampedModelMixin, models.Model):
    """
    A movie itself, not an occasion on which it was watched.

    Get a MovieEvent's creators:

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


class MovieEvent(BaseEvent):
    """
    An occasion on which a Movie was watched.
    """
    movie = models.ForeignKey('Movie', null=False, blank=False)

    def __str__(self):
        return "{} on {}".format(self.movie, self.date)


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

