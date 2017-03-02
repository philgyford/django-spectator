from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from spectator.admin import BookAdmin, PlayAdmin, PlayProductionAdmin
from spectator.factories import BookFactory, BookRoleFactory,\
        PlayFactory, PlayProductionFactory,\
        PlayProductionRoleFactory, PlayRoleFactory,\
        IndividualCreatorFactory
from spectator.models import Book, Play, PlayProduction


class AdminTestCase(TestCase):

    def setUp(self):
        self.site = AdminSite()


class BookAdminTestCase(AdminTestCase):

    def test_show_creators_with_roles(self):
        "When a Book has roles, display them."
        book = BookFactory()
        BookRoleFactory(
                book=book,
                creator=IndividualCreatorFactory(name='Bob'),
                role_order=1)
        BookRoleFactory(
                book=book,
                creator=IndividualCreatorFactory(name='Terry'),
                role_order=2)

        ba = BookAdmin(Book, self.site)
        self.assertEqual(ba.show_creators(book), 'Bob, Terry')

    def test_show_creators_no_roles(self):
        "When a Book has no roles, display '-'."
        book = BookFactory()

        ba = BookAdmin(Book, self.site)
        self.assertEqual(ba.show_creators(book), '-')


class PlayAdminTestCase(AdminTestCase):

    def test_show_creators_with_roles(self):
        "When a Play has roles, display them."
        play = PlayFactory()
        PlayRoleFactory(
                play=play,
                creator=IndividualCreatorFactory(name='Bob'),
                role_order=1)
        PlayRoleFactory(
                play=play,
                creator=IndividualCreatorFactory(name='Terry'),
                role_order=2)

        pa = PlayAdmin(Play, self.site)
        self.assertEqual(pa.show_creators(play), 'Bob, Terry')

    def test_show_creators_no_roles(self):
        "When a Play has no roles, display '-'."
        play = PlayFactory()

        pa = PlayAdmin(Play, self.site)
        self.assertEqual(pa.show_creators(play), '-')


class PlayProductionAdminTestCase(AdminTestCase):

    def test_show_creators_with_two_roles(self):
        "When a PlayProduction has roles, display them."
        production = PlayProductionFactory()
        PlayProductionRoleFactory(
                production=production,
                creator=IndividualCreatorFactory(name='Bob'),
                role_order=1)
        PlayProductionRoleFactory(
                production=production,
                creator=IndividualCreatorFactory(name='Terry'),
                role_order=2)

        ppa = PlayProductionAdmin(PlayProduction, self.site)
        self.assertEqual(ppa.show_creators(production), 'Bob, Terry')

    def test_show_creators_with_more_than_three_roles(self):
        "When a PlayProduction has many roles, display one."
        production = PlayProductionFactory()
        PlayProductionRoleFactory(
                production=production,
                creator=IndividualCreatorFactory(name='Bob'),
                role_order=1)
        PlayProductionRoleFactory(
                production=production,
                creator=IndividualCreatorFactory(name='Terry'),
                role_order=2)
        PlayProductionRoleFactory(
                production=production,
                creator=IndividualCreatorFactory(name='Audrey'),
                role_order=3)
        PlayProductionRoleFactory(
                production=production,
                creator=IndividualCreatorFactory(name='Thelma'),
                role_order=4)

        ppa = PlayProductionAdmin(PlayProduction, self.site)
        self.assertEqual(ppa.show_creators(production), 'Bob et al.')

    def test_show_creators_no_roles(self):
        "When a PlayProduction has no roles, display '-'."
        production = PlayProductionFactory()

        ppa = PlayProductionAdmin(PlayProduction, self.site)
        self.assertEqual(ppa.show_creators(production), '-')


