from distutils.version import StrictVersion
from unittest.mock import Mock, patch

from django import get_version
from django.http import QueryDict
from django.test import TestCase

from spectator.core.apps import Apps
from spectator.core.templatetags.spectator_core import domain_urlize,\
        get_enabled_apps, get_item, change_object_link_card, query_string
from spectator.core.factories import IndividualCreatorFactory


class GetEnabledAppsTestCase(TestCase):

    @patch.object(Apps, 'all')
    def test_results(self, patched_all):
        # all() will return an app that is not installed:
        patched_all.return_value = [
                        'events', 'reading', 'NOPE',]

        # So 'NOPE' shouldn't be returned here:
        enabled_apps = get_enabled_apps()
        self.assertEqual(2, len(enabled_apps))
        self.assertEqual(enabled_apps[0], 'events')
        self.assertEqual(enabled_apps[1], 'reading')


class GetItemTestCase(TestCase):

    def test_key(self):
        dict = {'a': 1,}
        self.assertEqual( get_item(dict, 'a'), 1)

    def test_key(self):
        dict = {'a': 1,}
        self.assertIsNone( get_item(dict, 'b') )


class DomainUrlizeTestCase(TestCase):

    def test_domain_urlize(self):
        self.assertEqual(
            domain_urlize('http://www.example.org/foo/'),
            '<a href="http://www.example.org/foo/" rel="nofollow">www.example.org</a>'
        )


class ChangeObjectLinkCardTestCase(TestCase):

    def test_output_can_change(self):
        creator = IndividualCreatorFactory(pk=5)
        perms = ['spectator.can_edit_creator',]

        result = change_object_link_card(creator, perms)
        self.assertTrue(result['display_link'])
        if get_version() < StrictVersion('1.9.0'):
            self.assertEqual(result['change_url'],
                    '/admin/spectator_core/creator/5/')
        else:
            self.assertEqual(result['change_url'],
                             '/admin/spectator_core/creator/5/change/')


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


