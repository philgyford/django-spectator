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

    def test_get_play_productions(self):
        bob = IndividualCreatorFactory()
        # Two productions. 1 role in the first, 2 in the second.
        p1 = PlayFactory(title='Play 1')
        pp1 = PlayProductionFactory(play=p1, title='Production 1')
        pprole1 = PlayProductionRoleFactory(
                production=pp1, creator=bob, role_name='Director')
        pp2 = PlayProductionFactory(play=p1, title='Production 2')
        pprole2 = PlayProductionRoleFactory(
                production=pp2, creator=bob, role_name='', role_order=2)
        pprole3 = PlayProductionRoleFactory(
                production=pp2, creator=bob, role_name='Actor', role_order=1)

        pps = bob.get_play_productions()
        self.assertEqual(len(pps), 2)

        self.assertEqual(pps[0], pp1)
        self.assertEqual(len(pps[0].creator_roles), 1)
        self.assertEqual(pps[0].creator_roles[0], pprole1)
        self.assertEqual(len(pps[0].creator_role_names), 1)
        self.assertEqual(pps[0].creator_role_names[0], 'Director')

        self.assertEqual(pps[1], pp2)
        self.assertEqual(len(pps[1].creator_roles), 2)
        self.assertEqual(pps[1].creator_roles[0], pprole3)
        self.assertEqual(pps[1].creator_roles[1], pprole2)
        self.assertEqual(len(pps[1].creator_role_names), 1)
        self.assertEqual(pps[1].creator_role_names[0], 'Actor')

    def test_get_plays_and_productions(self):
        bob = IndividualCreatorFactory()

        # One play, which Bob worked on:
        p1 = PlayFactory(title='Play 1')
        prole1 = PlayRoleFactory(play=p1, creator=bob, role_name='Writer')
        # And two productions of it, which Bob worked on:
        pp1a = PlayProductionFactory(play=p1, title='Production 1a')
        pprole1a = PlayProductionRoleFactory(
                production=pp1a, creator=bob, role_name='Director')
        pp1b = PlayProductionFactory(play=p1, title='Production 1b')
        pprole1b = PlayProductionRoleFactory(
                production=pp1b, creator=bob, role_name='Actor')

        # Another play which Bob worked on:
        p2 = PlayFactory(title='Play 2')
        prole2 = PlayRoleFactory(play=p2, creator=bob, role_name='Playwright')
        # And a Production which Bob DIDN'T work on:
        pp2 = PlayProductionFactory(play=p2, title='Production 2')
        pprole2 = PlayProductionRoleFactory(
                production=pp2, role_name='Director')

        # And a play which Bob DIDN'T work on:
        p3 = PlayFactory(title='Play 3')
        # But a Production of it which he DID:
        pp3 = PlayProductionFactory(play=p3, title='Production 3')
        pprole3 = PlayProductionRoleFactory(
                production=pp3, creator=bob, role_name='Producer')
        
        paps = bob.get_plays_and_productions()
        self.assertEqual(len(paps), 3)

        self.assertEqual(paps[0]['play'], p1)
        self.assertEqual(len(paps[0]['productions']), 2)
        self.assertEqual(paps[0]['productions'][0], pp1a)
        self.assertEqual(paps[0]['productions'][1], pp1b)

        self.assertEqual(len(paps[0]['play'].creator_roles), 1)
        self.assertEqual(paps[0]['play'].creator_roles[0], prole1)
        self.assertEqual(len(paps[0]['play'].creator_role_names), 1)
        self.assertEqual(paps[0]['play'].creator_role_names[0], 'Writer')

        self.assertEqual(len(paps[0]['productions'][0].creator_roles), 1)
        self.assertEqual(len(paps[0]['productions'][1].creator_roles), 1)

        self.assertEqual(paps[1]['play'], p2)
        self.assertEqual(len(paps[1]['productions']), 0)

        self.assertEqual(paps[2]['play'], p3)
        self.assertEqual(len(paps[2]['productions']), 1)

