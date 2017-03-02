from django.db import models

from . import BaseRole, Creator, TimeStampedModelMixin


class BaseEvent(TimeStampedModelMixin, models.Model):
    """
    Parent class for different kinds of event.
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
    Linking a creator to a concert, optionally via their role (e.g.
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
