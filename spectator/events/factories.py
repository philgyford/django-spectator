import factory

from . import models
from spectator.core.factories import IndividualCreatorFactory


class VenueFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Venue

    name = factory.Sequence(lambda n: 'Venue %s' % n)


class MovieFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Movie

    title = factory.Sequence(lambda n: 'Movie %s' % n)


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


class PlayRoleFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.PlayRole

    role_name = factory.Sequence(lambda n: 'Role %s' % n)
    creator = factory.SubFactory(IndividualCreatorFactory)
    play = factory.SubFactory(PlayFactory)


class EventFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Event

    title = factory.Sequence(lambda n: 'Event %s' % n)
    venue = factory.SubFactory(VenueFactory)

class GigEventFactory(EventFactory):
    kind = 'gig'

class MiscEventFactory(EventFactory):
    kind = 'misc'

class MovieEventFactory(EventFactory):
    kind = 'movie'
    movie = factory.SubFactory(MovieFactory)

class PlayEventFactory(EventFactory):
    kind = 'play'
    play = factory.SubFactory(PlayFactory)


class EventRoleFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.EventRole

    role_name = factory.Sequence(lambda n: 'Role %s' % n)
    creator = factory.SubFactory(IndividualCreatorFactory)
    event = factory.SubFactory(EventFactory)
