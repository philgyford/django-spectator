import factory

from . import models


class IndividualCreatorFactory(factory.django.DjangoModelFactory):
    "A creator that is an individual person."
    class Meta:
        model = models.Creator

    name = factory.Sequence(lambda n: 'Individual %s' % n)
    kind = 'individual'


class GroupCreatorFactory(factory.django.DjangoModelFactory):
    "A creator that is a group/organisation/etc."
    class Meta:
        model = models.Creator

    name = factory.Sequence(lambda n: 'Group %s' % n)
    kind = 'group'
