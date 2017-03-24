import factory

from . import models


# Factories for core models.

class IndividualCreatorFactory(factory.DjangoModelFactory):
    "A creator that is an individual person."
    class Meta:
        model = models.Creator

    name = factory.Sequence(lambda n: 'Individual %s' % n)
    kind = 'individual'


class GroupCreatorFactory(factory.DjangoModelFactory):
    "A creator that is a group/organisation/etc."
    class Meta:
        model = models.Creator

    name = factory.Sequence(lambda n: 'Group %s' % n)
    kind = 'group'


# Factories for publication models.

class PublicationSeriesFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.PublicationSeries

    title = factory.Sequence(lambda n: 'Publication Series %s' % n)


class PublicationFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Publication

    title = factory.Sequence(lambda n: 'Publication %s' % n)
    series = factory.SubFactory(PublicationSeriesFactory)


class PublicationRoleFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.PublicationRole

    role_name = factory.Sequence(lambda n: 'Role %s' % n)
    creator = factory.SubFactory(IndividualCreatorFactory)
    publication = factory.SubFactory(PublicationFactory)


class ReadingFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Reading

    publication = factory.SubFactory(PublicationFactory)


# Factories for event models.

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


