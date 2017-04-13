from django.core.exceptions import ValidationError
from django.test import TestCase

from .. import make_date
from spectator.core.factories import *
from spectator.events.factories import *
from spectator.events.models import Event, Movie, Play, Venue


class EventStrTestCase(TestCase):
    "Only testing the Event.__str__() method."

    def test_str_with_title(self):
        "If event has a title, that should be used."
        band = GroupCreatorFactory(name='Martha')
        event = GigEventFactory(title='Indietracks 2017')
        EventRoleFactory(event=event, creator=band)
        self.assertEqual(str(event), 'Indietracks 2017')

    def test_str_with_no_title_or_creators(self):
        "With no title or creator names, it still has a __str__"
        event = GigEventFactory(title='')
        self.assertEqual(str(event), 'Event #{}'.format(event.pk))

    def test_str_with_no_title_one_creator(self):
        event = GigEventFactory(title='')
        EventRoleFactory(
                event=event,
                creator=GroupCreatorFactory(name='Martha'),
                role_name='Headliner')
        self.assertEqual(str(event), 'Martha')

    def test_str_with_no_title_several_creators(self):
        "If event has no title, creator names should be used."
        event = GigEventFactory(title='')
        EventRoleFactory(
                event=event,
                creator=GroupCreatorFactory(name='Milky Wimpshake'),
                role_name='Headliner', role_order=1)
        EventRoleFactory(
                event=event,
                creator=GroupCreatorFactory(name='The Tuts'),
                role_name='Support', role_order=3)
        EventRoleFactory(
                event=event,
                creator=GroupCreatorFactory(name='Martha'),
                role_name='Support', role_order=2)
        self.assertEqual(str(event), 'Milky Wimpshake, Martha and The Tuts')

    # Concert

    def test_str_concert_with_title(self):
        event = ConcertEventFactory(title='Amazing Concert!')
        self.assertEqual(str(event), 'Amazing Concert!')

    def test_str_concert_with_no_title_one_work(self):
        "With no title and one work, it uses the work's title."
        event = ConcertEventFactory(
                        title='',
                        classicalworks=[ClassicalWorkFactory(title='Work A')])
        self.assertEqual(str(event), 'Work A')

    def test_str_concert_with_no_title_many_works(self):
        "With no title it uses the titles of the classical works."
        event = ConcertEventFactory(
                        title='',
                        classicalworks=[ClassicalWorkFactory(title='Work A'),
                                        ClassicalWorkFactory(title='Work B'),
                                        ClassicalWorkFactory(title='Work C')])
        self.assertEqual(str(event), 'Work A, Work B and Work C')

    def test_str_concert_with_no_title_and_no_works(self):
        "With no title or works it uses the default."
        event = ConcertEventFactory(title='', pk=5, classicalworks=[])
        self.assertEqual(str(event), 'Concert #5')

    # Dance

    def test_str_dance_with_title(self):
        event = DanceEventFactory(title='Amazing Dance!')
        self.assertEqual(str(event), 'Amazing Dance!')

    def test_str_dance_with_no_title_and_one_pieces(self):
        "With no title and one piece it uses the piece's title."
        event = DanceEventFactory(
                        title='',
                        dancepieces=[DancePieceFactory(title='Piece A')])
        self.assertEqual(str(event), 'Piece A')

    def test_str_dance_with_no_title_and_many_pieces(self):
        "With no title it uses the titles of the pieces."
        event = DanceEventFactory(
                        title='',
                        dancepieces=[DancePieceFactory(title='Piece A'),
                                     DancePieceFactory(title='Piece B'),
                                     DancePieceFactory(title='Piece C')])
        self.assertEqual(str(event), 'Piece A, Piece B and Piece C')

    def test_str_dance_with_no_title_and_no_pieces(self):
        "With no title or pieces it uses the default."
        event = DanceEventFactory(title='', pk=5, dancepieces=[])
        self.assertEqual(str(event), 'Dance #5')

    # Movie

    def test_movie_with_no_title(self):
        event = MovieEventFactory(title='',
                                  movie=MovieFactory(title='My Great Movie'))
        self.assertEqual(str(event), 'My Great Movie')

    # Play

    def test_play_with_no_title(self):
        event = PlayEventFactory(title='',
                                 play=PlayFactory(title='My Great Play'))
        self.assertEqual(str(event), 'My Great Play')


class EventTestCase(TestCase):
    "Testing everything except the __str__() method."

    def test_title_sort_with_no_title(self):
        "If there's no title, title_sort should be based on creators."
        event = GigEventFactory(title='')
        role1 = EventRoleFactory(
                event=event,
                creator=GroupCreatorFactory(name='Milky Wimpshake'),
                role_order=1)
        role2 = EventRoleFactory(
                event=event,
                creator=GroupCreatorFactory(name='Martha'),
                role_order=2)

        event.refresh_from_db()
        self.assertEqual(event.title_sort, 'milky wimpshake and martha')

        # And check it updates after deleting a relationship:
        role2.delete()
        event.refresh_from_db()
        self.assertEqual(event.title_sort, 'milky wimpshake')

    def test_get_kinds(self):
        self.assertEqual(
            Event.get_kinds(),
            ['concert', 'comedy', 'dance', 'exhibition', 'gig', 'misc',
                    'movie', 'play',]
        )

    def test_valid_kind_slugs(self):
        self.assertEqual(
            sorted(Event.get_valid_kind_slugs()),
            sorted(
                ['comedy', 'concerts', 'dance', 'exhibitions', 'gigs', 'misc',
                    'movies', 'plays',]
            )
        )

    def test_kind_slug(self):
        "Should be set on save."
        self.assertEqual(ComedyEventFactory().kind_slug, 'comedy')
        self.assertEqual(ConcertEventFactory().kind_slug, 'concerts')
        self.assertEqual(DanceEventFactory().kind_slug, 'dance')
        self.assertEqual(ExhibitionEventFactory().kind_slug, 'exhibitions')
        self.assertEqual(GigEventFactory().kind_slug, 'gigs')
        self.assertEqual(MiscEventFactory().kind_slug, 'misc')
        self.assertEqual(MovieEventFactory().kind_slug, 'movies')
        self.assertEqual(PlayEventFactory().kind_slug, 'plays')

    def test_kind_name(self):
        self.assertEqual(ComedyEventFactory().kind_name, 'Comedy')
        self.assertEqual(ConcertEventFactory().kind_name, 'Classical concert')
        self.assertEqual(DanceEventFactory().kind_name, 'Dance')
        self.assertEqual(ExhibitionEventFactory().kind_name, 'Exhibition')
        self.assertEqual(GigEventFactory().kind_name, 'Gig')
        self.assertEqual(MiscEventFactory().kind_name, 'Other')
        self.assertEqual(MovieEventFactory().kind_name, 'Movie')
        self.assertEqual(PlayEventFactory().kind_name, 'Play')

    def test_kind_name_plural(self):
        self.assertEqual(ComedyEventFactory().kind_name_plural, 'Comedy')
        self.assertEqual(ConcertEventFactory().kind_name_plural,
                                                        'Classical concerts')
        self.assertEqual(DanceEventFactory().kind_name_plural, 'Dance')
        self.assertEqual(ExhibitionEventFactory().kind_name_plural,
                                                                'Exhibitions')
        self.assertEqual(GigEventFactory().kind_name_plural, 'Gigs')
        self.assertEqual(MiscEventFactory().kind_name_plural, 'Others')
        self.assertEqual(MovieEventFactory().kind_name_plural, 'Movies')
        self.assertEqual(PlayEventFactory().kind_name_plural, 'Plays')

    def test_get_kinds_data(self):
        # Not exhaustively testing every part of the data returned...
        data = Event.get_kinds_data()
        self.assertEqual(len(data), 8)
        self.assertEqual(data['gig']['name'], 'Gig')
        self.assertEqual(data['gig']['slug'], 'gigs')
        self.assertEqual(data['gig']['name_plural'], 'Gigs')

    def test_ordering(self):
        "Should order by -date by default."
        e2 = GigEventFactory(title='Event', date=make_date('2017-02-01'))
        e3 = GigEventFactory(title='Abba Event', date=make_date('2017-01-01'))
        e1 = GigEventFactory(title='The Big Event',
                                                date=make_date('2017-03-01'))
        events = Event.objects.all()
        self.assertEqual(events[0], e1)
        self.assertEqual(events[1], e2)
        self.assertEqual(events[2], e3)

    def test_title_sort_ordering(self):
        "Should order by title_sort"
        e3 = GigEventFactory(title='Event')
        e1 = GigEventFactory(title='Abba Event')
        e2 = GigEventFactory(title='The Big Event')
        events = Event.objects.all().order_by('title_sort')
        self.assertEqual(events[0], e1)
        self.assertEqual(events[1], e2)
        self.assertEqual(events[2], e3)

    def test_roles(self):
        "It can have multiple EventRoles."
        bob = IndividualCreatorFactory(name='Bob')
        martha = GroupCreatorFactory(name='Martha')
        event = GigEventFactory()
        bobs_role = EventRoleFactory(event=event, creator=bob,
                                        role_name='Supporter', role_order=2)
        marthas_role = EventRoleFactory(event=event, creator=martha,
                                        role_name='Headliner', role_order=1)
        roles = event.roles.all()
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0], marthas_role)
        self.assertEqual(roles[1], bobs_role)
        self.assertEqual(roles[0].role_name, 'Headliner')
        self.assertEqual(roles[1].role_name, 'Supporter')

    def test_absolute_url_comedy(self):
        event = ComedyEventFactory(pk=3)
        self.assertEqual(event.get_absolute_url(), '/events/comedy/3/')

    def test_absolute_url_concert(self):
        event = ConcertEventFactory(pk=3)
        self.assertEqual(event.get_absolute_url(), '/events/concerts/3/')

    def test_absolute_url_dance(self):
        event = DanceEventFactory(pk=3)
        self.assertEqual(event.get_absolute_url(), '/events/dance/3/')

    def test_absolute_url_exhibition(self):
        event = ExhibitionEventFactory(pk=3)
        self.assertEqual(event.get_absolute_url(), '/events/exhibitions/3/')

    def test_absolute_url_gig(self):
        event = GigEventFactory(pk=3)
        self.assertEqual(event.get_absolute_url(), '/events/gigs/3/')

    def test_absolute_url_misc(self):
        event = MiscEventFactory(pk=3)
        self.assertEqual(event.get_absolute_url(), '/events/misc/3/')

    def test_absolute_url_movie(self):
        event = MovieEventFactory(pk=3, movie=MovieFactory(pk=6))
        self.assertEqual(event.get_absolute_url(), '/events/movies/6/')

    def test_absolute_url_play(self):
        event = PlayEventFactory(pk=3, play=PlayFactory(pk=6))
        self.assertEqual(event.get_absolute_url(), '/events/plays/6/')


class ClassicalWorkTestCase(TestCase):

    def test_get_absolute_url(self):
        work = ClassicalWorkFactory(pk=3)
        self.assertEqual(work.get_absolute_url(), '/events/concerts/works/3/')


class DancePieceTestCase(TestCase):

    def test_get_absolute_url(self):
        piece = DancePieceFactory(pk=3)
        self.assertEqual(piece.get_absolute_url(), '/events/dance/pieces/3/')


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

    def test_absolute_url(self):
        movie = MovieFactory(pk=3)
        self.assertEqual(movie.get_absolute_url(), '/events/movies/3/')


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

    def test_absolute_url(self):
        play = PlayFactory(pk=3)
        self.assertEqual(play.get_absolute_url(), '/events/plays/3/')



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

    def test_absolute_url(self):
        venue = VenueFactory(pk=3)
        self.assertEqual(venue.get_absolute_url(), '/events/venues/3/')

    def test_country_name_yes(self):
        venue = VenueFactory(country='GB')
        self.assertEqual(venue.country_name, 'UK')

    def test_country_name_no(self):
        venue = VenueFactory(country='')
        self.assertEqual(venue.country_name, None)

