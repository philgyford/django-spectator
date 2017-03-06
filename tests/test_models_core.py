# coding: utf-8
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


