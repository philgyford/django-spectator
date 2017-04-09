from unittest.mock import Mock

from django.http import QueryDict
from django.test import TestCase

from spectator.core.templatetags.spectator_core import domain_urlize,\
        query_string


class DomainUrlizeTestCase(TestCase):

    def test_domain_urlize(self):
        self.assertEqual(
            domain_urlize('http://www.example.org/foo/'),
            '<a href="http://www.example.org/foo/" rel="nofollow">www.example.org</a>'
        )


class QueryStringTestCase(TestCase):

    def test_adds_arg(self):
        "It adds your key/value to the existing GET string."
        context = {'request': Mock( GET=QueryDict('a=1') ) }
        self.assertIn(
            query_string(context, 'foo', 'bar'),
            ['foo=bar&a=1', 'a=1&foo=bar']
        )

    def test_replaces_arg(self):
        "It replaces an existing GET arg with what you supply."
        context = {'request': Mock( GET=QueryDict('a=1') ) }
        self.assertEqual(
            query_string(context, 'a', 'bar'),
            'a=bar'
        )

    def test_handles_missing_request(self):
        "If there's no request object, it doesn't complain."
        context = {}
        self.assertEqual(
            query_string(context, 'foo', 'bar'),
            'foo=bar'
        )

    def test_urlencodes(self):
        "It URL-encodes the returned string."
        context = {'request': Mock( GET=QueryDict('a=1') ) }
        self.assertIn(
            query_string(context, 'foo', 'bar&bar'),
            ['foo=bar%26bar&a=1', 'a=1&foo=bar%26bar']
        )


