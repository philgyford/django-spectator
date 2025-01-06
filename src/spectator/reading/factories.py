import factory

from spectator.core.factories import IndividualCreatorFactory

from . import models


class PublicationSeriesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PublicationSeries

    title = factory.Sequence(lambda n: f"Publication Series {n}")


class PublicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Publication

    title = factory.Sequence(lambda n: f"Publication {n}")
    series = factory.SubFactory(PublicationSeriesFactory)
    # Bigger width/height than default detail_thumbnail_2x size:
    thumbnail = factory.django.ImageField(color="blue", width=800, height=800)


class PublicationRoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PublicationRole

    role_name = factory.Sequence(lambda n: f"Role {n}")
    creator = factory.SubFactory(IndividualCreatorFactory)
    publication = factory.SubFactory(PublicationFactory)


class ReadingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Reading

    publication = factory.SubFactory(PublicationFactory)
