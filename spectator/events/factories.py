import factory

from . import models
from spectator.core.factories import IndividualCreatorFactory


class VenueFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Venue

    name = factory.Sequence(lambda n: 'Venue %s' % n)


class WorkFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Work

    title = factory.Sequence(lambda n: 'Work %s' % n)

class ClassicalWorkFactory(WorkFactory):
    kind = 'classicalwork'
    title = factory.Sequence(lambda n: 'Classical Work %s' % n)

class DancePieceFactory(WorkFactory):
    kind = 'dancepiece'
    title = factory.Sequence(lambda n: 'Dance Piece %s' % n)

class MovieFactory(WorkFactory):
    kind = 'movie'
    title = factory.Sequence(lambda n: 'Movie %s' % n)

class PlayFactory(WorkFactory):
    kind = 'play'
    title = factory.Sequence(lambda n: 'Play %s' % n)


class WorkRoleFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.WorkRole

    role_name = factory.Sequence(lambda n: 'Role %s' % n)
    creator = factory.SubFactory(IndividualCreatorFactory)
    work = factory.SubFactory(WorkFactory)


class EventFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Event

    title = factory.Sequence(lambda n: 'Event %s' % n)
    venue = factory.SubFactory(VenueFactory)


class ComedyEventFactory(EventFactory):
    kind = 'comedy'

class ConcertEventFactory(EventFactory):
    kind = 'concert'

class DanceEventFactory(EventFactory):
    kind = 'dance'

class ExhibitionEventFactory(EventFactory):
    kind = 'exhibition'

class GigEventFactory(EventFactory):
    kind = 'gig'

class MiscEventFactory(EventFactory):
    kind = 'misc'

class MovieEventFactory(EventFactory):
    kind = 'movie'

class PlayEventFactory(EventFactory):
    kind = 'play'


class EventRoleFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.EventRole

    role_name = factory.Sequence(lambda n: 'Role %s' % n)
    creator = factory.SubFactory(IndividualCreatorFactory)
    event = factory.SubFactory(EventFactory)


class WorkSelectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.WorkSelection

    event = factory.SubFactory(EventFactory)
    work = factory.SubFactory(WorkFactory)
