# coding: utf-8
from unittest.mock import patch

from django.test import TestCase

from spectator.factories import *
from spectator.models import Creator


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

    @patch('spectator.models.core.make_sort_name')
    def test_sort_name(self, make_sort_name):
        "It should call the make_sort_name method when saving."
        make_sort_name.return_value = "Jones, Bob"
        IndividualCreatorFactory(name='Bob Jones')
        make_sort_name.assert_called_once_with('Bob Jones', 'person')

