from django.test import TestCase
try:
    # Django >= 1.10
    from django.urls import resolve, reverse
except ImportError:
    # Django < 1.10
    from django.core.urlresolvers import resolve, reverse

from spectator.core import views
from spectator.core.factories import IndividualCreatorFactory


# Testing that the named URLs map the correct name to URL,
# and that the correct views are called.


class CoreUrlsTestCase(TestCase):

    def test_home_url(self):
        self.assertEqual(reverse('spectator:core:home'), '/')

    def test_home_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/').func.__name__,
                         views.HomeView.__name__)


    def test_creator_list_url(self):
        self.assertEqual(reverse('spectator:creators:creator_list'),
                                                                '/creators/')

    def test_creator_list_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/creators/').func.__name__,
                         views.CreatorListView.__name__)

    def test_creator_list_group_url(self):
        self.assertEqual(reverse('spectator:creators:creator_list_group'),
                         '/creators/groups/')

    def test_creator_list_group_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/creators/groups/').func.__name__,
                         views.CreatorListView.__name__)


    def test_creator_detail_url(self):
        IndividualCreatorFactory(pk=3)
        self.assertEqual(reverse('spectator:creators:creator_detail', kwargs={'pk': 3}),
                        '/creators/3/')

    def test_creator_detail_view(self):
        "Should use the correct view."
        IndividualCreatorFactory(pk=3)
        self.assertEqual(resolve('/creators/3/').func.__name__,
                         views.CreatorDetailView.__name__)

