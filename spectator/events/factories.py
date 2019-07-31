import factory

from . import models
from spectator.core.factories import IndividualCreatorFactory


class VenueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Venue

    name = factory.Sequence(lambda n: "Venue %s" % n)


class WorkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Work

    title = factory.Sequence(lambda n: "Work %s" % n)


class ClassicalWorkFactory(WorkFactory):
    kind = "classicalwork"
    title = factory.Sequence(lambda n: "Classical Work %s" % n)


class DancePieceFactory(WorkFactory):
    kind = "dancepiece"
    title = factory.Sequence(lambda n: "Dance Piece %s" % n)


class ExhibitionFactory(WorkFactory):
    kind = "exhibition"
    title = factory.Sequence(lambda n: "Exhibition %s" % n)


class MovieFactory(WorkFactory):
    kind = "movie"
    title = factory.Sequence(lambda n: "Movie %s" % n)


class PlayFactory(WorkFactory):
    kind = "play"
    title = factory.Sequence(lambda n: "Play %s" % n)


class WorkRoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorkRole

    role_name = factory.Sequence(lambda n: "Role %s" % n)
    creator = factory.SubFactory(IndividualCreatorFactory)
    work = factory.SubFactory(WorkFactory)


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Event

    title = factory.Sequence(lambda n: "Event %s" % n)
    venue = factory.SubFactory(VenueFactory)
    ticket = factory.django.ImageField(color="blue")


class ComedyEventFactory(EventFactory):
    kind = "comedy"


class ConcertEventFactory(EventFactory):
    kind = "concert"


class DanceEventFactory(EventFactory):
    kind = "dance"


class MuseumEventFactory(EventFactory):
    kind = "museum"


class GigEventFactory(EventFactory):
    kind = "gig"


class MiscEventFactory(EventFactory):
    kind = "misc"


class CinemaEventFactory(EventFactory):
    kind = "cinema"


class TheatreEventFactory(EventFactory):
    kind = "theatre"


class EventRoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EventRole

    role_name = factory.Sequence(lambda n: "Role %s" % n)
    creator = factory.SubFactory(IndividualCreatorFactory)
    event = factory.SubFactory(MiscEventFactory)


class WorkSelectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorkSelection

    event = factory.SubFactory(MiscEventFactory)
    work = factory.SubFactory(WorkFactory)
