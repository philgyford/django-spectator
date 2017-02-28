import factory

from . import models


class IndividualCreatorFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Creator

    name = factory.Sequence(lambda n: 'Individual %s' % n)
    kind = 'individual'


class GroupCreatorFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Creator

    name = factory.Sequence(lambda n: 'Group %s' % n)
    kind = 'group'



class BookSeriesFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.BookSeries

    title = factory.Sequence(lambda n: 'Book Series %s' % n)


class BookFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Book

    title = factory.Sequence(lambda n: 'Book Title %s' % n)
    series = factory.SubFactory(BookSeriesFactory)


class RoleFactory(factory.DjangoModelFactory):
    "You probably want to use a child of this class."
    class Meta:
        model = models.Role

    creator = factory.SubFactory(IndividualCreatorFactory)
    role_name = factory.Sequence(lambda n: 'Role %s' % n)


class BookRoleFactory(RoleFactory):
    content_object = factory.SubFactory(BookFactory)
