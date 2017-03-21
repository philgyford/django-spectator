from django.test import TestCase

from . import make_date
from spectator.factories import *
from spectator.models import Concert, Movie, MovieEvent,\
        Play, PlayProduction, PlayProductionEvent, Venue


class EventTestCase(TestCase):
    "Testing the parent class."

    def test_str(self):
        e = EventFactory()
        self.assertEqual(str(e), 'Event #{}'.format(e.pk))


class ConcertTestCase(TestCase):

    def test_str_with_title(self):
        "If concert has a title, that should be used."
        band = GroupCreatorFactory(name='Martha')
        concert = ConcertFactory(title='Indietracks 2017')
        ConcertRoleFactory(concert=concert, creator=band)
        self.assertEqual(str(concert), 'Indietracks 2017')

    def test_str_with_no_title_or_creators(self):
        "With no title or band names, it still has a __str__"
        concert = ConcertFactory(title='')
        self.assertEqual(str(concert), 'Concert #{}'.format(concert.pk))

    def test_str_with_no_title_one_creator(self):
        concert = ConcertFactory(title='')
        ConcertRoleFactory(
                concert=concert,
                creator=GroupCreatorFactory(name='Martha'),
                role_name='Headliner')
        self.assertEqual(str(concert), 'Martha')

    def test_str_with_no_title_several_creators(self):
        "If concert has no title, band names should be used."
        concert = ConcertFactory(title='')
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
        "Should order by title_sort"
        c3 = ConcertFactory(title='Concert')
        c1 = ConcertFactory(title='Abba Concert')
        c2 = ConcertFactory(title='The Big Concert')
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

