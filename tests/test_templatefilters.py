from django.test import TestCase

from spectator.templatetags.spectator_filters import domain_urlize


class DomainUrlizeTestCase(TestCase):

    def test_domain_urlize(self):
        self.assertEqual(
            domain_urlize('http://www.example.org/foo/'),
            '<a href="http://www.example.org/foo/" rel="nofollow">www.example.org</a>'
        )

