from distutils.version import StrictVersion
from unittest.mock import Mock, patch

from django import get_version
from django.http import QueryDict
from django.test import TestCase

from .. import make_date

from spectator.core.apps import Apps
from spectator.core.templatetags.spectator_core import (
    domain_urlize,
    get_enabled_apps,
    get_item,
    change_object_link_card,
    most_read_creators,
    most_read_creators_card,
    most_visited_venues,
    most_visited_venues_card,
    query_string,
)
from spectator.core.factories import IndividualCreatorFactory
from spectator.events.factories import MiscEventFactory, VenueFactory
from spectator.reading.factories import (
    PublicationFactory,
    PublicationRoleFactory,
    ReadingFactory,
)


class GetEnabledAppsTestCase(TestCase):
    @patch.object(Apps, "all")
    def test_results(self, patched_all):
        # all() will return an app that is not installed:
        patched_all.return_value = ["events", "reading", "NOPE"]

        # So 'NOPE' shouldn't be returned here:
        enabled_apps = get_enabled_apps()
        self.assertEqual(2, len(enabled_apps))
        self.assertEqual(enabled_apps[0], "events")
        self.assertEqual(enabled_apps[1], "reading")


class GetItemTestCase(TestCase):
    def test_key(self):
        dict = {"a": 1}
        self.assertEqual(get_item(dict, "a"), 1)

    def test_key_none(self):
        dict = {"a": 1}
        self.assertIsNone(get_item(dict, "b"))


class DomainUrlizeTestCase(TestCase):
    def test_domain_urlize(self):
        self.assertEqual(
            domain_urlize("http://www.example.org/foo/"),
            '<a href="http://www.example.org/foo/" rel="nofollow">example.org</a>',
        )


class ChangeObjectLinkCardTestCase(TestCase):
    def test_output_can_change(self):
        creator = IndividualCreatorFactory(pk=5)
        perms = ["spectator.can_edit_creator"]

        result = change_object_link_card(creator, perms)
        self.assertTrue(result["display_link"])
        if get_version() < StrictVersion("1.9.0"):
            self.assertEqual(result["change_url"], "/admin/spectator_core/creator/5/")
        else:
            self.assertEqual(
                result["change_url"], "/admin/spectator_core/creator/5/change/"
            )


class QueryStringTestCase(TestCase):
    def test_adds_arg(self):
        "It adds your key/value to the existing GET string."
        context = {"request": Mock(GET=QueryDict("a=1"))}
        self.assertIn(
            query_string(context, "foo", "bar"), ["foo=bar&a=1", "a=1&foo=bar"]
        )

    def test_replaces_arg(self):
        "It replaces an existing GET arg with what you supply."
        context = {"request": Mock(GET=QueryDict("a=1"))}
        self.assertEqual(query_string(context, "a", "bar"), "a=bar")

    def test_handles_missing_request(self):
        "If there's no request object, it doesn't complain."
        context = {}
        self.assertEqual(query_string(context, "foo", "bar"), "foo=bar")

    def test_urlencodes(self):
        "It URL-encodes the returned string."
        context = {"request": Mock(GET=QueryDict("a=1"))}
        self.assertIn(
            query_string(context, "foo", "bar&bar"),
            ["foo=bar%26bar&a=1", "a=1&foo=bar%26bar"],
        )


class MostReadCreatorsTestCase(TestCase):
    def test_returns_queryset(self):
        "It should return 10 items by default."
        d = make_date("2017-02-15")

        for i in range(11):
            c = IndividualCreatorFactory()
            pub = PublicationFactory()
            PublicationRoleFactory(publication=pub, creator=c, role_name="")
            ReadingFactory(publication=pub, start_date=d, end_date=d, is_finished=True)

        creators = most_read_creators()

        self.assertEqual(len(creators), 10)

    def test_num(self):
        "It should return `num` items."
        d = make_date("2017-02-15")

        for i in range(4):
            c = IndividualCreatorFactory()
            pub = PublicationFactory()
            PublicationRoleFactory(publication=pub, creator=c, role_name="")
            ReadingFactory(publication=pub, start_date=d, end_date=d, is_finished=True)

        creators = most_read_creators(num=3)

        self.assertEqual(len(creators), 3)

    def test_finished(self):
        "It should only return finished readings"
        d = make_date("2017-02-15")

        # A finished reading
        c1 = IndividualCreatorFactory()
        pub1 = PublicationFactory()
        PublicationRoleFactory(publication=pub1, creator=c1, role_name="")
        ReadingFactory(publication=pub1, start_date=d, end_date=d, is_finished=True)
        ReadingFactory(publication=pub1, start_date=d, end_date=d, is_finished=True)
        ReadingFactory(publication=pub1, start_date=d, end_date=d, is_finished=False)

        # An unfinished reading
        c2 = IndividualCreatorFactory()
        pub2 = PublicationFactory()
        PublicationRoleFactory(publication=pub2, creator=c2, role_name="")
        ReadingFactory(publication=pub2, start_date=d, end_date=d, is_finished=False)

        creators = most_read_creators()

        self.assertEqual(len(creators), 1)
        self.assertEqual(creators[0], c1)
        self.assertEqual(creators[0].num_readings, 2)


class MostReadCreatorsCardTestCase(TestCase):
    def test_returns_correct_data(self):
        d = make_date("2017-02-15")

        for i in range(2, 13):
            c = IndividualCreatorFactory()
            pub = PublicationFactory()
            PublicationRoleFactory(publication=pub, creator=c, role_name="")
            # It'll cut off any with only 1 reading, so:
            ReadingFactory.create_batch(
                i, publication=pub, start_date=d, end_date=d, is_finished=True
            )

        data = most_read_creators_card()

        self.assertIn("card_title", data)
        self.assertIn("score_attr", data)
        self.assertIn("object_list", data)

        self.assertEqual(data["card_title"], "Most read authors")
        self.assertEqual(data["score_attr"], "num_readings")
        self.assertEqual(len(data["object_list"]), 10)

    def test_num(self):
        "It should return `num` items."
        d = make_date("2017-02-15")

        for i in range(2, 6):
            c = IndividualCreatorFactory()
            pub = PublicationFactory()
            PublicationRoleFactory(publication=pub, creator=c, role_name="")
            # It'll cut off any with only 1 reading, so:
            ReadingFactory.create_batch(
                i, publication=pub, start_date=d, end_date=d, is_finished=True
            )

        data = most_read_creators_card(num=3)

        self.assertIn("object_list", data)
        self.assertEqual(len(data["object_list"]), 3)

    def test_finished(self):
        "It should only return finished readings"
        d = make_date("2017-02-15")

        # A finished reading
        c1 = IndividualCreatorFactory()
        pub1 = PublicationFactory()
        PublicationRoleFactory(publication=pub1, creator=c1, role_name="")
        # It'll cut off any with only 1 reading, so:
        ReadingFactory.create_batch(
            3, publication=pub1, start_date=d, end_date=d, is_finished=True
        )

        # Another finished reading (so there's a chart)
        c2 = IndividualCreatorFactory()
        pub2 = PublicationFactory()
        PublicationRoleFactory(publication=pub2, creator=c2, role_name="")
        # It'll cut off any with only 1 reading, so:
        ReadingFactory.create_batch(
            2, publication=pub2, start_date=d, end_date=d, is_finished=True
        )
        # An unfinished reading for the same author - they should still be in the
        # chart though, because they have one finished reading.
        ReadingFactory(publication=pub2, start_date=d, end_date=d, is_finished=False)

        # An unfinished reading
        c3 = IndividualCreatorFactory()
        pub3 = PublicationFactory()
        PublicationRoleFactory(publication=pub3, creator=c3, role_name="")
        # It'll cut off any with only 1 reading, so:
        ReadingFactory.create_batch(
            2, publication=pub3, start_date=d, end_date=d, is_finished=False
        )

        data = most_read_creators_card()

        self.assertIn("object_list", data)
        self.assertEqual(len(data["object_list"]), 2)
        self.assertEqual(data["object_list"][0], c1)
        self.assertEqual(data["object_list"][0].num_readings, 3)
        self.assertEqual(data["object_list"][1], c2)
        self.assertEqual(data["object_list"][1].num_readings, 2)


class MostVisitedVenuesTestCase(TestCase):
    def test_returns_queryset(self):
        "It should return 10 items by default."
        for i in range(11):
            MiscEventFactory(venue=VenueFactory())

        venues = most_visited_venues()

        self.assertEqual(len(venues), 10)

    def test_num(self):
        "It should return `num` items."
        for i in range(4):
            MiscEventFactory(venue=VenueFactory())

        venues = most_visited_venues(num=3)

        self.assertEqual(len(venues), 3)


class MostVisitedVenuesCardTestCase(TestCase):
    def test_returns_correct_data(self):
        for i in range(2, 13):
            # It'll cut off any with only 1 reading, so:
            MiscEventFactory.create_batch(i, venue=VenueFactory())

        data = most_visited_venues_card()

        self.assertIn("card_title", data)
        self.assertIn("score_attr", data)
        self.assertIn("object_list", data)

        self.assertEqual(data["card_title"], "Most visited venues")
        self.assertEqual(data["score_attr"], "num_visits")
        self.assertEqual(len(data["object_list"]), 10)

    def test_num(self):
        "It should return `num` items."
        for i in range(2, 6):
            # It'll cut off any with only 1 reading, so:
            MiscEventFactory.create_batch(i, venue=VenueFactory())

        data = most_visited_venues_card(num=3)

        self.assertIn("object_list", data)
        self.assertEqual(len(data["object_list"]), 3)
