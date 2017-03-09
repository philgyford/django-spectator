# coding: utf-8
from django.test import TestCase

from spectator.utils import make_sort_name


class UtilsTestCase(TestCase):

    def test_thing_no_change(self):
        "If name doesn't start with an article, sort_name should be identical."
        self.assertEqual(make_sort_name('LCD Soundsystem', 'thing'),
                                        'LCD Soundsystem')

    def test_thing_the(self):
        "If name starts with 'The' sort_name should have it at the end."
        self.assertEqual(make_sort_name('The Long Blondes', 'thing'),
                                        'Long Blondes, The')

    def test_thing_a(self):
        "If name starts with 'A' sort_name should have it at the end."
        self.assertEqual(make_sort_name('A Group Name', 'thing'),
                                        'Group Name, A')

    def test_thing_a_dot(self):
        "If name starts with 'A.' sort_name should have it at the start."
        self.assertEqual(make_sort_name('A. B. Group', 'thing'),
                                        'A. B. Group')

    def test_person_one_word(self):
        "If name is one word sort_name should be the same"
        self.assertEqual(make_sort_name('Prince', 'person'),
                                        'Prince')

    def test_person_two_words(self):
        "If name is two names, sort_name should be 'Surname, Firstname'"
        self.assertEqual(make_sort_name('Alice Faye', 'person'),
                                        'Faye, Alice')

    def test_person_three_words(self):
        "If name is three names, sort_name should be 'Surname, First Second'"
        self.assertEqual(make_sort_name('David Foster Wallace', 'person'),
                                        'Wallace, David Foster')

    def test_person_suffix(self):
        "If name has a suffix, it should not be first in sort_name"
        self.assertEqual(make_sort_name('Billy Q Smith Jr', 'person'),
                                        'Smith, Billy Q Jr')

    def test_person_suffix_two_words(self):
        "If name has a suffix, but only two words, sort_name should be the same"
        self.assertEqual(make_sort_name('Bill Jr.', 'person'),
                                        'Bill Jr.')

    def test_person_uppercase_particle(self):
        "Uses an upper case particle like 'Le' as part of the surname."
        self.assertEqual(make_sort_name('John Le Carré', 'person'),
                                        'Le Carré, John')

    def test_person_lowercase_particle(self):
        "Does not use a lower case particle like 'du' as part of the surname."
        self.assertEqual(make_sort_name('Daphne du Maurier', 'person'),
                                        'Maurier, Daphne du')

