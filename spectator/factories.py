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

