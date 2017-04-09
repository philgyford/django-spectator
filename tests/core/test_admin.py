from django.contrib.admin.sites import AdminSite
from django.test import TestCase


class AdminTestCase(TestCase):
    "For all other admin test cases to inherit from."

    def setUp(self):
        self.site = AdminSite()

