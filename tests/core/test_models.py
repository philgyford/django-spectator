# coding: utf-8
from django.test import TestCase

from spectator.core.factories import *
from spectator.events.factories import *
from spectator.reading.factories import *
from spectator.core.models import Creator


class CreatorTestCase(TestCase):

    def test_str(self):
        creator = IndividualCreatorFactory(name='Bill Brown')
        self.assertEqual(str(creator), 'Bill Brown')

    def test_ordering(self):
        # Will have a name_sort of 'peaness':
        b = IndividualCreatorFactory(name='Peaness')
        # Will have a name_sort of 'long blondes, the':
        a = IndividualCreatorFactory(name='The Long Blondes')
        creators = Creator.objects.all()
        self.assertEqual(creators[0], a)
        self.assertEqual(creators[1], b)

    def test_absolute_url(self):
        creator = IndividualCreatorFactory(pk=3)
        self.assertEqual(creator.get_absolute_url(), '/creators/3/')

    def test_publication_roles(self):
        bob = IndividualCreatorFactory(name='Bob')
        pub1 = PublicationFactory(title='Publication 1')
        pub2 = PublicationFactory(title='Publication 2')
        role1 = PublicationRoleFactory(
                        publication=pub1, creator=bob, role_name='Author')
        role2 = PublicationRoleFactory(
                        publication=pub2, creator=bob, role_name='Editor')
        roles = bob.publication_roles.all()
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0], role1)
        self.assertEqual(roles[1], role2)
        self.assertEqual(roles[0].role_name, 'Author')
        self.assertEqual(roles[1].role_name, 'Editor')

    def test_event_roles(self):
        bob = IndividualCreatorFactory(name='Bob')
        event1 = GigEventFactory()
        event2 = GigEventFactory()
        role1 = EventRoleFactory(
                        event=event1, creator=bob, role_name='Headliner')
        role2 = EventRoleFactory(
                        event=event2, creator=bob, role_name='Support')
        roles = bob.event_roles.all()
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

    def test_get_movies(self):
        bob = IndividualCreatorFactory()
        # Two movies. 1 role in the first, 2 in the second.
        m1 = MovieFactory(title='Movie 1')
        mrole1 = MovieRoleFactory(movie=m1, creator=bob, role_name='Writer')
        m2 = MovieFactory(title='Movie 2')
        mrole2 = MovieRoleFactory(
                    movie=m2, creator=bob, role_name='Director', role_order=1)
        mrole3 = MovieRoleFactory(
                    movie=m2, creator=bob, role_name='', role_order=2)

        movies = bob.get_movies()
        self.assertEqual(len(movies), 2)

        self.assertEqual(movies[0], m1)
        self.assertEqual(len(movies[0].creator_roles), 1)
        self.assertEqual(movies[0].creator_roles[0], mrole1)
        self.assertEqual(len(movies[0].creator_role_names), 1)
        self.assertEqual(movies[0].creator_role_names[0], 'Writer')

        self.assertEqual(movies[1], m2)
        self.assertEqual(len(movies[1].creator_roles), 2)
        self.assertEqual(movies[1].creator_roles[0], mrole2)
        self.assertEqual(movies[1].creator_roles[1], mrole3)
        self.assertEqual(len(movies[1].creator_role_names), 1)
        self.assertEqual(movies[1].creator_role_names[0], 'Director')

    def test_get_plays(self):
        bob = IndividualCreatorFactory()
        # Two plays. 1 role in the first, 2 in the second.
        p1 = PlayFactory(title='Play 1')
        prole1 = PlayRoleFactory(play=p1, creator=bob, role_name='Writer')
        p2 = PlayFactory(title='Play 2')
        prole2 = PlayRoleFactory(
                        play=p2, creator=bob, role_name='Author', role_order=1)
        prole3 = PlayRoleFactory(
                        play=p2, creator=bob, role_name='', role_order=2)

        plays = bob.get_plays()
        self.assertEqual(len(plays), 2)

        self.assertEqual(plays[0], p1)
        self.assertEqual(len(plays[0].creator_roles), 1)
        self.assertEqual(plays[0].creator_roles[0], prole1)
        self.assertEqual(len(plays[0].creator_role_names), 1)
        self.assertEqual(plays[0].creator_role_names[0], 'Writer')

        self.assertEqual(plays[1], p2)
        self.assertEqual(len(plays[1].creator_roles), 2)
        self.assertEqual(plays[1].creator_roles[0], prole2)
        self.assertEqual(plays[1].creator_roles[1], prole3)
        self.assertEqual(len(plays[1].creator_role_names), 1)
        self.assertEqual(plays[1].creator_role_names[0], 'Author')

