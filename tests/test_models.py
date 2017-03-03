# coding: utf-8
from datetime import datetime
from django.test import TestCase

from spectator.factories import *
from spectator.models import Book, Concert, Creator, Movie, MovieEvent,\
        Play, PlayProduction, PlayProductionEvent, Reading, Venue


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
        self.assertEqual(roles[0].role_name, 'Author')
        self.assertEqual(roles[1].role_name, 'Editor')

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
        self.assertEqual(roles[0].role_name, 'Headliner')
        self.assertEqual(roles[1].role_name, 'Support')

    def test_movie_roles(self):
        bob = IndividualCreatorFactory(name='Bob')
        movie1 = MovieFactory()
        movie2 = MovieFactory()
        role1 = MovieRoleFactory(
                        movie=movie1, creator=bob,
                        role_name='Director', role_order=1)
        role2 = MovieRoleFactory(
                        movie=movie2, creator=bob,
                        role_name='Actor', role_order=2)
        roles = bob.movie_roles.all()
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0], role1)
        self.assertEqual(roles[1], role2)
        self.assertEqual(roles[0].role_name, 'Director')
        self.assertEqual(roles[1].role_name, 'Actor')

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
        self.assertEqual(roles[0].role_name, 'Author')
        self.assertEqual(roles[1].role_name, 'Editor')


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


class EventTestCase(TestCase):
    "Testing the parent class."

    def test_str_with_no_title(self):
        e = EventFactory()
        self.assertEqual(str(e), 'Event #{}'.format(e.pk))


class ConcertTestCase(TestCase):

    def test_str_with_concert_title(self):
        "If concert has a concert_title, that should be used."
        band = GroupCreatorFactory(name='Martha')
        concert = ConcertFactory(concert_title='Indietracks 2017')
        ConcertRoleFactory(concert=concert, creator=band)
        self.assertEqual(str(concert), 'Indietracks 2017')

    def test_str_with_no_concert_title_or_creators(self):
        "With no concert_title or band names, it still has a __str__"
        concert = ConcertFactory(concert_title='')
        self.assertEqual(str(concert), 'Concert #{}'.format(concert.pk))

    def test_str_with_no_concert_title_one_creator(self):
        concert = ConcertFactory(concert_title='')
        ConcertRoleFactory(
                concert=concert,
                creator=GroupCreatorFactory(name='Martha'),
                role_name='Headliner')
        self.assertEqual(str(concert), 'Martha')

    def test_str_with_no_concert_title_several_creators(self):
        "If concert has no concert_title, band names should be used."
        concert = ConcertFactory(concert_title='')
        ConcertRoleFactory(
                concert=concert,
                creator=GroupCreatorFactory(name='Milky Wimpshake'),
                role_name='Headliner', role_order=1)
        ConcertRoleFactory(
                concert=concert,
                creator=GroupCreatorFactory(name='The Tuts'),
                role_name='Support', role_order=3)
        ConcertRoleFactory(
                concert=concert,
                creator=GroupCreatorFactory(name='Martha'),
                role_name='Support', role_order=2)
        self.assertEqual(str(concert), 'Milky Wimpshake, Martha and The Tuts')

    def test_ordering(self):
        "Should order by date"
        c3 = ConcertFactory(date=make_date('2017-02-28'))
        c1 = ConcertFactory(date=make_date('2016-06-28'))
        c2 = ConcertFactory(date=make_date('2016-12-28'))
        concerts = Concert.objects.all()
        self.assertEqual(concerts[0], c1)
        self.assertEqual(concerts[1], c2)
        self.assertEqual(concerts[2], c3)

    def test_save_sets_title(self):
        "On save, the title should be set."
        c = ConcertFactory(concert_title="My Concert")
        self.assertEqual(c.title, str(c))

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
        self.assertEqual(roles[0].role_name, 'Headliner')
        self.assertEqual(roles[1].role_name, 'Supporter')


class MovieTestCase(TestCase):

    def test_str_with_year(self):
        movie = MovieFactory(title='Trust', year=1991)
        self.assertEqual(str(movie), 'Trust (1991)')

    def test_str_without_year(self):
        movie = MovieFactory(title='Trust')
        self.assertEqual(str(movie), 'Trust')

    def test_ordering(self):
        m3 = MovieFactory(title='Movie C')
        m1 = MovieFactory(title='Movie A')
        m2 = MovieFactory(title='Movie B')
        movies = Movie.objects.all()
        self.assertEqual(movies[0], m1)
        self.assertEqual(movies[1], m2)
        self.assertEqual(movies[2], m3)

    def test_roles(self):
        "It can have multiple MovieRoles."
        bob = IndividualCreatorFactory(name='Bob')
        terry = IndividualCreatorFactory(name='Terry')
        movie = MovieFactory()
        bobs_role = MovieRoleFactory(movie=movie, creator=bob,
                                        role_name='Actor', role_order=2)
        terrys_role = MovieRoleFactory(movie=movie, creator=terry,
                                        role_name='Director', role_order=1)
        roles = movie.roles.all()
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0], terrys_role)
        self.assertEqual(roles[1], bobs_role)
        self.assertEqual(roles[0].role_name, 'Director')
        self.assertEqual(roles[1].role_name, 'Actor')


class MovieEventTestCase(TestCase):

    def test_str(self):
        m = MovieFactory(title="Trust")
        me = MovieEventFactory(movie=m, date=make_date('2017-02-28'))
        self.assertEqual(str(me), 'Trust')

    def test_ordering(self):
        "Should order by date"
        me3 = MovieEventFactory(date=make_date('2017-02-28'))
        me1 = MovieEventFactory(date=make_date('2016-06-28'))
        me2 = MovieEventFactory(date=make_date('2016-12-28'))
        movie_events = MovieEvent.objects.all()
        self.assertEqual(movie_events[0], me1)
        self.assertEqual(movie_events[1], me2)
        self.assertEqual(movie_events[2], me3)

    def test_save_sets_title(self):
        "On save, the title should be set."
        me = MovieEventFactory()
        self.assertEqual(me.title, str(me))


class PlayTestCase(TestCase):

    def test_str(self):
        play = PlayFactory(title='Twelfth Night')
        self.assertEqual(str(play), 'Twelfth Night')

    def test_ordering(self):
        p3 = PlayFactory(title='Play C')
        p1 = PlayFactory(title='Play A')
        p2 = PlayFactory(title='Play B')
        plays = Play.objects.all()
        self.assertEqual(plays[0], p1)
        self.assertEqual(plays[1], p2)
        self.assertEqual(plays[2], p3)

    def test_roles(self):
        "It can have multiple PlayRoles."
        bob = IndividualCreatorFactory(name='Bob')
        terry = IndividualCreatorFactory(name='Terry')
        play = PlayFactory()
        bobs_role = PlayRoleFactory(play=play, creator=bob,
                                        role_name='Author', role_order=2)
        terrys_role = PlayRoleFactory(play=play, creator=terry,
                                        role_name='Author', role_order=1)
        roles = play.roles.all()
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0], terrys_role)
        self.assertEqual(roles[1], bobs_role)
        self.assertEqual(roles[0].role_name, 'Author')
        self.assertEqual(roles[1].role_name, 'Author')


class PlayProductionTestCase(TestCase):

    def test_str_with_title(self):
        production = PlayProductionFactory(
                            play=PlayFactory(title='Twelfth Night'),
                            title='Special Production')
        self.assertEqual(str(production), 'Special Production')

    def test_str_with_no_title_no_creators(self):
        production = PlayProductionFactory(
                            play=PlayFactory(title='Twelfth Night'),
                            title='')
        self.assertEqual(str(production), 'Production of Twelfth Night')

    def test_str_with_no_title_one_creator(self):
        production = PlayProductionFactory(
                            play=PlayFactory(title='Twelfth Night'),
                            title='')
        PlayProductionRoleFactory(production=production,
                            creator=IndividualCreatorFactory(name='Bob'))
        self.assertEqual(str(production), 'Twelfth Night by Bob')

    def test_str_with_no_title_several_creators(self):
        production = PlayProductionFactory(
                            play=PlayFactory(title='Twelfth Night'),
                            title='')
        PlayProductionRoleFactory(production=production,
                            creator=IndividualCreatorFactory(name='Bob'),
                            role_order=2)
        PlayProductionRoleFactory(production=production,
                            creator=IndividualCreatorFactory(name='Terry'),
                            role_order=1)
        self.assertEqual(str(production), 'Twelfth Night by Terry et al.')

    def test_ordering(self):
        p3 = PlayProductionFactory(play=PlayFactory(title='Play C'))
        p1 = PlayProductionFactory(play=PlayFactory(title='Play A'))
        p2 = PlayProductionFactory(play=PlayFactory(title='Play B'))
        productions = PlayProduction.objects.all()
        self.assertEqual(productions[0], p1)
        self.assertEqual(productions[1], p2)
        self.assertEqual(productions[2], p3)

    def test_roles(self):
        "It can have multiple PlayProductionRoles."
        bob = IndividualCreatorFactory(name='Bob')
        terry = IndividualCreatorFactory(name='Terry')
        production = PlayProductionFactory()
        bobs_role = PlayProductionRoleFactory(production=production,
                            creator=bob, role_name='Actor', role_order=2)
        terrys_role = PlayProductionRoleFactory(production=production,
                            creator=terry, role_name='Director', role_order=1)
        roles = production.roles.all()
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0], terrys_role)
        self.assertEqual(roles[1], bobs_role)
        self.assertEqual(roles[0].role_name, 'Director')
        self.assertEqual(roles[1].role_name, 'Actor')


class PlayProductionEventTestCase(TestCase):

    def test_str(self):
        pp = PlayProductionFactory(title='Special Production')
        ppe = PlayProductionEventFactory(production=pp)
        self.assertEqual(str(ppe), 'Special Production')

    def test_ordering(self):
        "Should order by date"
        ppe3 = PlayProductionEventFactory(date=make_date('2017-02-28'))
        ppe1 = PlayProductionEventFactory(date=make_date('2016-06-28'))
        ppe2 = PlayProductionEventFactory(date=make_date('2016-12-28'))
        production_events = PlayProductionEvent.objects.all()
        self.assertEqual(production_events[0], ppe1)
        self.assertEqual(production_events[1], ppe2)
        self.assertEqual(production_events[2], ppe3)

    def test_save_sets_title(self):
        "On save, the title should be set."
        ppe = PlayProductionEventFactory()
        self.assertEqual(ppe.title, str(ppe))


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

