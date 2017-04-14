from django.core.exceptions import ValidationError
from django.test import TestCase

from .. import make_date
from ..core.test_admin import AdminTestCase
from spectator.core.factories import IndividualCreatorFactory
from spectator.events.admin import EventAdminForm, MovieAdmin, PlayAdmin
from spectator.events.factories import ClassicalWorkFactory,\
        DancePieceFactory, MovieFactory, MovieRoleFactory, PlayFactory,\
        PlayRoleFactory, VenueFactory
from spectator.events.models import Movie, Play


class EventAdminFormTestCase(TestCase):

    def test_clean_classicalworks_valid(self):
        "No error when a concert has classicalworks."
        form = EventAdminForm({'kind': 'concert',
                               'classicalworks': [ClassicalWorkFactory().pk]})
        self.assertNotIn('classicalworks', form.errors)

    def test_clean_classicalworks_no_works(self):
        "Error when a concert has no classicalworks."
        form = EventAdminForm({'kind': 'concert'})
        self.assertIn('classicalworks', form.errors)

    def test_clean_classicalworks_not_concert(self):
        "Error when not-a-concert has classicalworks."
        form = EventAdminForm({'kind': 'movie',
                               'classicalworks': [ClassicalWorkFactory().pk]})
        self.assertIn('classicalworks', form.errors)

    def test_clean_dancepieces_valid(self):
        "No error when a dance has dancepieces."
        form = EventAdminForm({'kind': 'dance',
                               'dancepieces': [DancePieceFactory().pk]})
        self.assertNotIn('dancepieces', form.errors)

    def test_clean_dancepieces_no_works(self):
        "Error when a dance has no dancepieces."
        form = EventAdminForm({'kind': 'dance'})
        self.assertIn('dancepieces', form.errors)

    def test_clean_dancepieces_not_dance(self):
        "Error when not-a-dance has dancepieces."
        form = EventAdminForm({'kind': 'movie',
                               'dancepieces': [DancePieceFactory().pk]})
        self.assertIn('dancepieces', form.errors)

    def test_clean_movie_event_valid(self):
        "No error when a movie event has a movie."
        movie = MovieFactory(pk=5)
        form = EventAdminForm({'kind': 'movie', 'movie': 5})
        self.assertNotIn('movie', form.errors)

    def test_clean_movie_event_no_movie(self):
        "Error when a movie event has no movie."
        form = EventAdminForm({'kind': 'movie'})
        self.assertIn('movie', form.errors)

    def test_clean_movie_not_movie_event(self):
        "Error when not-a-movie event has a movie."
        movie = MovieFactory(pk=5)
        form = EventAdminForm({'kind': 'gig', 'movie': 5})
        self.assertIn('movie', form.errors)

    def test_clean_play_event_valid(self):
        "No error when a play event has a play."
        play = PlayFactory(pk=5)
        form = EventAdminForm({'kind': 'play', 'play': 5})
        self.assertNotIn('play', form.errors)

    def test_clean_play_event_no_play(self):
        "Error when a play event has no play."
        form = EventAdminForm({'kind': 'play'})
        self.assertIn('play', form.errors)

    def test_clean_play_not_play_event(self):
        "Error when not-a-play event has a play."
        play = PlayFactory(pk=5)
        form = EventAdminForm({'kind': 'gig', 'play': 5})
        self.assertIn('play', form.errors)


class MovieAdminTestCase(AdminTestCase):

    def test_show_creators_with_roles(self):
        "When a Movie has roles, display them."
        movie = MovieFactory()
        MovieRoleFactory(
                movie=movie,
                creator=IndividualCreatorFactory(name='Bob'),
                role_order=1)
        MovieRoleFactory(
                movie=movie,
                creator=IndividualCreatorFactory(name='Terry'),
                role_order=2)

        pa = MovieAdmin(Movie, self.site)
        self.assertEqual(pa.show_creators(movie), 'Bob, Terry')

    def test_show_creators_no_roles(self):
        "When a Movie has no roles, display '-'."
        movie = MovieFactory()
        pa = MovieAdmin(Movie, self.site)
        self.assertEqual(pa.show_creators(movie), '-')

    def test_show_creators_many_roles(self):
        "When a Movie has many roles, only show the first."
        movie = MovieFactory()
        MovieRoleFactory(
                movie=movie,
                creator=IndividualCreatorFactory(name='Bob'),
                role_order=1)
        MovieRoleFactory(
                movie=movie,
                creator=IndividualCreatorFactory(name='Terry'),
                role_order=2)
        MovieRoleFactory(
                movie=movie,
                creator=IndividualCreatorFactory(name='Thelma'),
                role_order=3)
        MovieRoleFactory(
                movie=movie,
                creator=IndividualCreatorFactory(name='Audrey'),
                role_order=4)

        pa = MovieAdmin(Movie, self.site)
        self.assertEqual(pa.show_creators(movie), 'Bob et al.')


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

    def test_show_creators_many_roles(self):
        "When a Play has many roles, only show the first."
        play = PlayFactory()
        PlayRoleFactory(
                play=play,
                creator=IndividualCreatorFactory(name='Bob'),
                role_order=1)
        PlayRoleFactory(
                play=play,
                creator=IndividualCreatorFactory(name='Terry'),
                role_order=2)
        PlayRoleFactory(
                play=play,
                creator=IndividualCreatorFactory(name='Thelma'),
                role_order=3)
        PlayRoleFactory(
                play=play,
                creator=IndividualCreatorFactory(name='Audrey'),
                role_order=4)
        pa = PlayAdmin(Play, self.site)
        self.assertEqual(pa.show_creators(play), 'Bob et al.')

