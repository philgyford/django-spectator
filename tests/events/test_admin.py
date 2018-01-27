from django.core.exceptions import ValidationError
from django.test import TestCase

from .. import make_date
from ..core.test_admin import AdminTestCase
from spectator.core.factories import IndividualCreatorFactory
from spectator.events.admin import MovieAdmin, PlayAdmin
from spectator.events.factories import ClassicalWorkFactory,\
        DancePieceFactory, MovieFactory, MovieRoleFactory, PlayFactory,\
        PlayRoleFactory, VenueFactory
from spectator.events.models import Movie, Play


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
