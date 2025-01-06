import factory

from spectator.core.factories import IndividualCreatorFactory

from . import models


class VenueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Venue

    name = factory.Sequence(lambda n: f"Venue {n}")


class WorkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Work

    title = factory.Sequence(lambda n: f"Work {n}")


class ClassicalWorkFactory(WorkFactory):
    kind = "classicalwork"
    title = factory.Sequence(lambda n: f"Classical Work {n}")


class DancePieceFactory(WorkFactory):
    kind = "dancepiece"
    title = factory.Sequence(lambda n: f"Dance Piece {n}")


class ExhibitionFactory(WorkFactory):
    kind = "exhibition"
    title = factory.Sequence(lambda n: f"Exhibition {n}")


class MovieFactory(WorkFactory):
    kind = "movie"
    title = factory.Sequence(lambda n: f"Movie {n}")


class PlayFactory(WorkFactory):
    kind = "play"
    title = factory.Sequence(lambda n: f"Play {n}")


class WorkRoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorkRole

    role_name = factory.Sequence(lambda n: f"Role {n}")
    creator = factory.SubFactory(IndividualCreatorFactory)
    work = factory.SubFactory(WorkFactory)


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Event

    title = factory.Sequence(lambda n: f"Event {n}")
    venue = factory.SubFactory(VenueFactory)
    # Bigger width/height than default detail_thumbnail_2x size:
    thumbnail = factory.django.ImageField(color="blue", width=800, height=800)


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

    role_name = factory.Sequence(lambda n: f"Role {n}")
    creator = factory.SubFactory(IndividualCreatorFactory)
    event = factory.SubFactory(MiscEventFactory)


class WorkSelectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.WorkSelection

    event = factory.SubFactory(MiscEventFactory)
    work = factory.SubFactory(WorkFactory)
