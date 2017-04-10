# coding: utf-8
from unittest.mock import call, patch

from django.test import TestCase
from django.apps import apps

from spectator.core.apps import Apps, spectator_apps


class SpectatorAppsTestCase(TestCase):

    def test_all(self):
        all_apps = spectator_apps.all()
        self.assertEqual(2, len(all_apps))
        self.assertEqual(all_apps[0], 'events')
        self.assertEqual(all_apps[1], 'reading')

    @patch.object(Apps, 'all')
    def test_installed(self, patched_all):
        # all() will return an app that is not installed:
        patched_all.return_value = [
                        'events', 'reading', 'NOPE',]

        # So 'NOPE' shouldn't be returned here:
        installed_apps = spectator_apps.installed()
        self.assertEqual(2, len(installed_apps))
        self.assertEqual(installed_apps[0], 'events')
        self.assertEqual(installed_apps[1], 'reading')

    @patch.object(Apps, 'all')
    def test_enabled(self, patched_all):
        # all() will return an app that is not installed:
        patched_all.return_value = [
                        'events', 'reading', 'NOPE',]

        # So 'NOPE' shouldn't be returned here:
        enabled_apps = spectator_apps.enabled()
        self.assertEqual(2, len(enabled_apps))
        self.assertEqual(enabled_apps[0], 'events')
        self.assertEqual(enabled_apps[1], 'reading')

    def test_is_installed(self):
        self.assertTrue(spectator_apps.is_installed('events'))
        self.assertFalse(spectator_apps.is_installed('NOPE'))

    def test_is_enabled(self):
        self.assertTrue(spectator_apps.is_enabled('events'))
        self.assertFalse(spectator_apps.is_enabled('NOPE'))


