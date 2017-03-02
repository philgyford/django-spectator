from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from spectator.admin import BookAdmin
from spectator.factories import BookFactory, BookRoleFactory,\
        IndividualCreatorFactory
from spectator.models import Book


class BookAdminTestCase(TestCase):

    def setUp(self):
        self.site = AdminSite()

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





