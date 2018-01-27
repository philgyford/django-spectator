import factory

from . import models
from spectator.core.factories import IndividualCreatorFactory


class VenueFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Venue

    name = factory.Sequence(lambda n: 'Venue %s' % n)


class ClassicalWorkFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.ClassicalWork

    title = factory.Sequence(lambda n: 'Classical Work %s' % n)

class ClassicalWorkRoleFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.ClassicalWorkRole

    role_name = factory.Sequence(lambda n: 'Role %s' % n)
    creator = factory.SubFactory(IndividualCreatorFactory)
    classical_work = factory.SubFactory(ClassicalWorkFactory)


class DancePieceFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.DancePiece

    title = factory.Sequence(lambda n: 'Dance Piece %s' % n)

class DancePieceRoleFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.DancePieceRole

    role_name = factory.Sequence(lambda n: 'Role %s' % n)
    creator = factory.SubFactory(IndividualCreatorFactory)
    dance_piece = factory.SubFactory(DancePieceFactory)


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


class ClassicalWorkSelectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.ClassicalWorkSelection

    event = factory.SubFactory(EventFactory)
    work = factory.SubFactory(ClassicalWorkFactory)

class DancePieceSelectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.DancePieceSelection

    event = factory.SubFactory(EventFactory)
    work = factory.SubFactory(DancePieceFactory)

class MovieSelectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.MovieSelection

    event = factory.SubFactory(EventFactory)
    work = factory.SubFactory(MovieFactory)

class PlaySelectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.PlaySelection

    event = factory.SubFactory(EventFactory)
    work = factory.SubFactory(PlayFactory)
