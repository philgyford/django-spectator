import factory

from . import models
from spectator.core.factories import IndividualCreatorFactory


class VenueFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Venue

    name = factory.Sequence(lambda n: 'Venue %s' % n)


class EventFactory(factory.DjangoModelFactory):
    "The parent event class"
    class Meta:
        model = models.Event

    venue = factory.SubFactory(VenueFactory)


class ConcertFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Concert

    title = factory.Sequence(lambda n: 'Concert %s' % n)
    venue = factory.SubFactory(VenueFactory)


class ConcertRoleFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.ConcertRole

    role_name = factory.Sequence(lambda n: 'Role %s' % n)
    creator = factory.SubFactory(IndividualCreatorFactory)
    concert = factory.SubFactory(ConcertFactory)


class MovieFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Movie

    title = factory.Sequence(lambda n: 'Movie %s' % n)


class MovieEventFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.MovieEvent

    movie = factory.SubFactory(MovieFactory)
    venue = factory.SubFactory(VenueFactory)


class MovieRoleFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.MovieRole

    role_name = factory.Sequence(lambda n: 'Role %s' % n)
    creator = factory.SubFactory(IndividualCreatorFactory)
    movie = factory.SubFactory(MovieFactory)


class PlayFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Play

    title = factory.Sequence(lambda n: 'Play %s' % n)


class PlayProductionFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.PlayProduction

    play = factory.SubFactory(PlayFactory)
    title = factory.Sequence(lambda n: 'Production %s' % n)


class PlayProductionEventFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.PlayProductionEvent

    production = factory.SubFactory(PlayProductionFactory)
    venue = factory.SubFactory(VenueFactory)


class PlayProductionRoleFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.PlayProductionRole

    role_name = factory.Sequence(lambda n: 'Role %s' % n)
    creator = factory.SubFactory(IndividualCreatorFactory)
    production = factory.SubFactory(PlayProductionFactory)


class PlayRoleFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.PlayRole

    role_name = factory.Sequence(lambda n: 'Role %s' % n)
    creator = factory.SubFactory(IndividualCreatorFactory)
    play = factory.SubFactory(PlayFactory)


class MiscEventFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.MiscEvent

    title = factory.Sequence(lambda n: 'Misc Event %s' % n)
    venue = factory.SubFactory(VenueFactory)


class MiscEventRoleFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.MiscEventRole

    role_name = factory.Sequence(lambda n: 'Role %s' % n)
    creator = factory.SubFactory(IndividualCreatorFactory)
    miscevent = factory.SubFactory(MiscEventFactory)


