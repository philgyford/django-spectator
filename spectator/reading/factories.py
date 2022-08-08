import factory

from spectator.core.factories import IndividualCreatorFactory

from . import models


class PublicationSeriesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PublicationSeries

    title = factory.Sequence(lambda n: "Publication Series %s" % n)


class PublicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Publication

    title = factory.Sequence(lambda n: "Publication %s" % n)
    series = factory.SubFactory(PublicationSeriesFactory)
    # Bigger width/height than default detail_thumbnail_2x size:
    thumbnail = factory.django.ImageField(color="blue", width=800, height=800)


class PublicationRoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PublicationRole

    role_name = factory.Sequence(lambda n: "Role %s" % n)
    creator = factory.SubFactory(IndividualCreatorFactory)
    publication = factory.SubFactory(PublicationFactory)


class ReadingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Reading

    publication = factory.SubFactory(PublicationFactory)
