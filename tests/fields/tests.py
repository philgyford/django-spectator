# coding: utf-8
from django.test import TestCase

from .models import PersonModel, TitleModel


class NaturalSortFieldTestCase(TestCase):
    "Testing the NaturalSortField field."

    def test_no_change(self):
        "If name doesn't start with an article, sort_name should be identical."
        obj = TitleModel.objects.create(title='LCD Soundsystem')
        obj.refresh_from_db()
        self.assertEqual(obj.title_sort, 'lcd soundsystem')

    def test_the(self):
        "If name starts with 'The' sort_name should have it at the end."
        obj = TitleModel.objects.create(title='The Long Blondes')
        obj.refresh_from_db()
        self.assertEqual(obj.title_sort, 'long blondes, the')

    def test_a(self):
        "If name starts with 'A' sort_name should have it at the end."
        obj = TitleModel.objects.create(title='A Group Name')
        obj.refresh_from_db()
        self.assertEqual(obj.title_sort, 'group name, a')

    def test_a_dot(self):
        "If name starts with 'A.' sort_name should have it at the start."
        obj = TitleModel.objects.create(title='A. B. Group')
        obj.refresh_from_db()
        self.assertEqual(obj.title_sort, 'a. b. group')

    def test_strip(self):
        "Spaces are stripped"
        obj = TitleModel.objects.create(title='  Fred  ')
        obj.refresh_from_db()
        self.assertEqual(obj.title_sort, 'fred')

    def test_numbers(self):
        "Numbers are zero-padded."
        obj = TitleModel.objects.create(title='Vol. 2 No. 11, November 2004')
        obj.refresh_from_db()
        self.assertEqual(obj.title_sort,
                        'vol. 00000002 no. 00000011, november 00002004')

    def test_la_la(self):
        "'La La Land' should not have a 'La' moved to the end."
        obj = TitleModel.objects.create(title='La La Land')
        obj.refresh_from_db()
        self.assertEqual(obj.title_sort, 'la la land')

    def test_the_the(self):
        "'The The' should not have a 'The' moved after a final comma."
        obj = TitleModel.objects.create(title='The The')
        obj.refresh_from_db()
        self.assertEqual(obj.title_sort, 'the the')


class PersonNaturalSortFieldTestCase(TestCase):
    "Testing the NaturalSortField field when used for a person."

    def test_one_word(self):
        "If name is one word sort_name should be the same"
        obj = PersonModel.objects.create(name='Prince')
        obj.refresh_from_db()
        self.assertEqual(obj.name_sort, 'prince')

    def test_two_words(self):
        "If name is two names, sort_name should be 'Surname, Firstname'"
        obj = PersonModel.objects.create(name='Alice Faye')
        obj.refresh_from_db()
        self.assertEqual(obj.name_sort, 'faye, alice')

    def test_three_words(self):
        "If name is three names, sort_name should be 'Surname, First Second'"
        obj = PersonModel.objects.create(name='David Foster Wallace')
        obj.refresh_from_db()
        self.assertEqual(obj.name_sort, 'wallace, david foster')

    def test_suffix(self):
        "If name has a suffix, it should not be first in sort_name"
        obj = PersonModel.objects.create(name='Billy Q Smith Jr')
        obj.refresh_from_db()
        self.assertEqual(obj.name_sort, 'smith, billy q jr')

    def test_suffix_two_words(self):
        "If name has a suffix, but only two words, sort_name should be the same"
        obj = PersonModel.objects.create(name='Bill Jr')
        obj.refresh_from_db()
        self.assertEqual(obj.name_sort, 'bill jr')

    def test_uppercase_particle(self):
        "Uses an upper case particle like 'Le' as part of the surname."
        obj = PersonModel.objects.create(name='John Le Carré')
        obj.refresh_from_db()
        self.assertEqual(obj.name_sort, 'le carré, john')

    def test_lowercase_particle(self):
        "Does not use a lower case particle like 'du' as part of the surname."
        obj = PersonModel.objects.create(name='Daphne du Maurier')
        obj.refresh_from_db()
        self.assertEqual(obj.name_sort, 'maurier, daphne du')

    def test_numbers(self):
        "Numbers are zero-padded."
        obj = PersonModel.objects.create(name='Bob 7')
        obj.refresh_from_db()
        self.assertEqual(obj.name_sort, '00000007, bob')

