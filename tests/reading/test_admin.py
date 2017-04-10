from django.test import TestCase

from .. import make_date
from ..core.test_admin import AdminTestCase
from spectator.core.factories import IndividualCreatorFactory
from spectator.reading.admin import PublicationAdmin
from spectator.reading.factories import PublicationFactory,\
        PublicationRoleFactory
from spectator.reading.models import Publication


class PublicationAdminTestCase(AdminTestCase):

    def test_show_creators_with_roles(self):
        "When a Publication has roles, display them."
        pub = PublicationFactory()
        PublicationRoleFactory(
                publication=pub,
                creator=IndividualCreatorFactory(name='Bob'),
                role_order=1)
        PublicationRoleFactory(
                publication=pub,
                creator=IndividualCreatorFactory(name='Terry'),
                role_order=2)

        ba = PublicationAdmin(Publication, self.site)
        self.assertEqual(ba.show_creators(pub), 'Bob, Terry')

    def test_show_creators_no_roles(self):
        "When a Publication has no roles, display '-'."
        pub = PublicationFactory()

        ba = PublicationAdmin(Publication, self.site)
        self.assertEqual(ba.show_creators(pub), '-')


