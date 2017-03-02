# coding: utf-8
from datetime import datetime
from django.test import TestCase

from spectator.factories import *
from spectator.models import Book, Concert, Creator, Reading, Venue


def make_date(d):
    "For convenience."
    return datetime.strptime(d, "%Y-%m-%d").date()


class CreatorTestCase(TestCase):

    def test_str(self):
        creator = IndividualCreatorFactory(name='Bill Brown')
        self.assertEqual(str(creator), 'Bill Brown')

    def test_ordering(self):
        b = IndividualCreatorFactory(sort_name='Brown, Bill')
        a = IndividualCreatorFactory(sort_name='Apple, Adam')
        creators = Creator.objects.all()
        self.assertEqual(creators[0], a)
        self.assertEqual(creators[1], b)

    def test_book_roles(self):
        bob = IndividualCreatorFactory(name='Bob')
        book1 = BookFactory(title='Book 1')
        book2 = BookFactory(title='Book 2')
        role1 = BookRoleFactory(book=book1, creator=bob, role_name='Author')
        role2 = BookRoleFactory(book=book2, creator=bob, role_name='Editor')
        roles = bob.book_roles.all()
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0], role1)
        self.assertEqual(roles[1], role2)

    def test_concert_roles(self):
        bob = IndividualCreatorFactory(name='Bob')
        concert1 = ConcertFactory()
        concert2 = ConcertFactory()
        role1 = ConcertRoleFactory(
                        concert=concert1, creator=bob, role_name='Headliner')
        role2 = ConcertRoleFactory(
                        concert=concert2, creator=bob, role_name='Support')
        roles = bob.concert_roles.all()
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0], role1)
        self.assertEqual(roles[1], role2)

    def test_group_sort_name(self):
        "If name doesn't start with an article, sort_name should be identical."
        group = GroupCreatorFactory(name='LCD Soundsystem')
        self.assertEqual(group.sort_name, 'LCD Soundsystem')

    def test_group_sort_name_the(self):
        "If name starts with 'The' sort_name should have it at the end."
        group = GroupCreatorFactory(name='The Long Blondes')
        self.assertEqual(group.sort_name, 'Long Blondes, The')

    def test_group_sort_name_a(self):
        "If name starts with 'A' sort_name should have it at the end."
        group = GroupCreatorFactory(name='A Group Name')
        self.assertEqual(group.sort_name, 'Group Name, A')

    def test_group_sort_name_a_dot(self):
        "If name starts with 'A.' sort_name should have it at the start."
        group = GroupCreatorFactory(name='A. B. Group')
        self.assertEqual(group.sort_name, 'A. B. Group')

    def test_individual_sort_name_one_word(self):
        "If name is one word sort_name should be the same"
        group = IndividualCreatorFactory(name='Prince')
        self.assertEqual(group.sort_name, 'Prince')

    def test_individual_sort_name_two_words(self):
        "If name is two names, sort_name should be 'Surname, Firstname'"
        group = IndividualCreatorFactory(name='Alice Faye')
        self.assertEqual(group.sort_name, 'Faye, Alice')

    def test_individual_sort_name_three_words(self):
        "If name is three names, sort_name should be 'Surname, First Second'"
        group = IndividualCreatorFactory(name='David Foster Wallace')
        self.assertEqual(group.sort_name, 'Wallace, David Foster')

    def test_individual_sort_name_suffix(self):
        "If name has a suffix, it should not be first in sort_name"
        group = IndividualCreatorFactory(name='Billy Q Smith Jr')
        self.assertEqual(group.sort_name, 'Smith, Billy Q Jr')

    def test_individual_sort_name_suffix_two_words(self):
        "If name has a suffix, but only two words, sort_name should be the same"
        group = IndividualCreatorFactory(name='Bill Jr.')
        self.assertEqual(group.sort_name, 'Bill Jr.')

    def test_individual_sort_name_uppercase_particle(self):
        "Uses an upper case particle like 'Le' as part of the surname."
        group = IndividualCreatorFactory(name='John Le Carré')
        self.assertEqual(group.sort_name, 'Le Carré, John')

    def test_individual_sort_name_lowercase_particle(self):
        "Does not use a lower case particle like 'du' as part of the surname."
        group = IndividualCreatorFactory(name='Daphne du Maurier')
        self.assertEqual(group.sort_name, 'Maurier, Daphne du')


class BookRoleTestCase(TestCase):

    def test_str_1(self):
        creator = IndividualCreatorFactory(name='Bill Brown')
        role = BookRoleFactory(creator=creator, role_name='')
        self.assertEqual(str(role), 'Bill Brown')

    def test_str_2(self):
        creator = IndividualCreatorFactory(name='Bill Brown')
        role = BookRoleFactory(creator=creator, role_name='Editor')
        self.assertEqual(str(role), 'Bill Brown (Editor)')


class BookSeriesTestCase(TestCase):

    def test_str(self):
        series = BookSeriesFactory(title='The London Review of Books')
        self.assertEqual(str(series), 'The London Review of Books')


class BookTestCase(TestCase):

    def test_str(self):
        book = BookFactory(title='Aurora')
        self.assertEqual(str(book), 'Aurora')

    def test_ordering(self):
        "Should order by book title."
        b3 = BookFactory(title='Book C')
        b1 = BookFactory(title='Book A')
        b2 = BookFactory(title='Book B')
        books = Book.objects.all()
        self.assertEqual(books[0], b1)
        self.assertEqual(books[1], b2)
        self.assertEqual(books[2], b3)

    def test_roles(self):
        "It can have multiple BookRoles."
        bob = IndividualCreatorFactory(name='Bob')
        terry = IndividualCreatorFactory(name='Terry')
        book = BookFactory()
        bobs_role = BookRoleFactory(book=book, creator=bob,
                                        role_name='Editor', role_order=2)
        terrys_role = BookRoleFactory(book=book, creator=terry,
                                        role_name='Author', role_order=1)
        roles = book.roles.all()
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0], terrys_role)
        self.assertEqual(roles[1], bobs_role)


class ReadingTestCase(TestCase):

    def test_str(self):
        reading = ReadingFactory(
                book=BookFactory(title='Big Book'),
                start_date=make_date('2017-02-15'),
                end_date=make_date('2017-02-28'),
            )
        self.assertEqual(str(reading), 'Big Book (2017-02-15 to 2017-02-28)')

    def test_ordering(self):
        reading1 = ReadingFactory(
                start_date=make_date('2017-02-15'),
                end_date=make_date('2017-02-28'),
            )
        reading2 = ReadingFactory(
                start_date=make_date('2017-01-15'),
                end_date=make_date('2017-01-28'),
            )
        readings = Reading.objects.all()
        self.assertEqual(readings[0], reading2)
        self.assertEqual(readings[1], reading1)


class ConcertTestCase(TestCase):

    def test_str_with_title(self):
        "If concert has a title, that should be used."
        band = GroupCreatorFactory(name='Martha')
        concert = ConcertFactory(title='Indietracks 2017')
        ConcertRoleFactory(concert=concert, creator=band)
        self.assertEqual(str(concert), 'Indietracks 2017')

    def test_str_with_no_title(self):
        "If concert has no title, band names should be used."
        b1 = GroupCreatorFactory(name='Martha')
        b2 = GroupCreatorFactory(name='Milky Wimpshake')
        b3 = GroupCreatorFactory(name='The Tuts')
        concert = ConcertFactory(title='')
        ConcertRoleFactory(concert=concert, creator=b1, role_name='Headliner',
                role_order=1)
        ConcertRoleFactory(concert=concert, creator=b2, role_name='Support',
                role_order=2)
        ConcertRoleFactory(concert=concert, creator=b3, role_name='Support',
                role_order=3)
        self.assertEqual(str(concert), 'Martha, Milky Wimpshake and The Tuts')

    def test_str_with_no_title_or_creators(self):
        "With no title or band names, it still has a __str__"
        concert = ConcertFactory(title='')
        self.assertEqual(str(concert), 'Concert <{}>'.format(concert.pk))

    def test_ordering(self):
        "Should order by date"
        c3 = ConcertFactory(date=make_date('2017-02-28'))
        c1 = ConcertFactory(date=make_date('2016-06-28'))
        c2 = ConcertFactory(date=make_date('2016-12-28'))
        concerts = Concert.objects.all()
        self.assertEqual(concerts[0], c1)
        self.assertEqual(concerts[1], c2)
        self.assertEqual(concerts[2], c3)

    def test_roles(self):
        "It can have multiple ConcertRoles."
        bob = IndividualCreatorFactory(name='Bob')
        martha = GroupCreatorFactory(name='Martha')
        concert = ConcertFactory()
        bobs_role = ConcertRoleFactory(concert=concert, creator=bob,
                                        role_name='Supporter', role_order=2)
        marthas_role = ConcertRoleFactory(concert=concert, creator=martha,
                                        role_name='Headliner', role_order=1)
        roles = concert.roles.all()
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0], marthas_role)
        self.assertEqual(roles[1], bobs_role)


class VenueTestCase(TestCase):

    def test_str(self):
        venue = VenueFactory(name='My Venue')
        self.assertEqual(str(venue), 'My Venue')

    def test_ordering(self):
        "Should order by venue name."
        v3 = VenueFactory(name='Venue C')
        v1 = VenueFactory(name='Venue A')
        v2 = VenueFactory(name='Venue B')
        venues = Venue.objects.all()
        self.assertEqual(venues[0], v1)
        self.assertEqual(venues[1], v2)
        self.assertEqual(venues[2], v3)

