import os

import piexif
from django.core.exceptions import ValidationError
from django.core.files import File
from django.test import TestCase, override_settings

from spectator.core.factories import IndividualCreatorFactory
from spectator.reading.factories import (
    PublicationFactory,
    PublicationRoleFactory,
    PublicationSeriesFactory,
    ReadingFactory,
)
from spectator.reading.models import Publication
from tests import make_date


class PublicationRoleTestCase(TestCase):
    def test_str_1(self):
        creator = IndividualCreatorFactory(name="Bill Brown")
        role = PublicationRoleFactory(creator=creator, role_name="")
        self.assertEqual(str(role), "Bill Brown")

    def test_str_2(self):
        creator = IndividualCreatorFactory(name="Bill Brown")
        role = PublicationRoleFactory(creator=creator, role_name="Editor")
        self.assertEqual(str(role), "Bill Brown (Editor)")


class PublicationSeriesTestCase(TestCase):
    def test_str(self):
        series = PublicationSeriesFactory(title="The London Review of Books")
        self.assertEqual(str(series), "The London Review of Books")

    def test_slug(self):
        series = PublicationSeriesFactory(pk=123)
        self.assertEqual(series.slug, "9g5o8")

    def test_absolute_url(self):
        series = PublicationSeriesFactory(pk=123)
        self.assertEqual(series.get_absolute_url(), "/reading/series/9g5o8/")


class PublicationTestCase(TestCase):
    def test_str(self):
        pub = PublicationFactory(title="Aurora")
        self.assertEqual(str(pub), "Aurora")

    def test_slug(self):
        pub = PublicationFactory(pk=123)
        self.assertEqual(pub.slug, "9g5o8")

    def test_ordering(self):
        "Should order by book title."
        b3 = PublicationFactory(title="Publication C")
        b1 = PublicationFactory(title="Publication A")
        b2 = PublicationFactory(title="Publication B")
        pubs = Publication.objects.all()
        self.assertEqual(pubs[0], b1)
        self.assertEqual(pubs[1], b2)
        self.assertEqual(pubs[2], b3)

    def test_absolute_url(self):
        pub = PublicationFactory(pk=123)
        self.assertEqual(pub.get_absolute_url(), "/reading/publications/9g5o8/")

    @override_settings(
        IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY="imagekit.cachefiles.strategies.Optimistic"
    )
    def test_thumbnail(self):
        """
        By default it should use reading/publications/{pub.slug}/ as the path.
        Ensure it works with the Optimistic cachefile strategy.
        """
        pub = PublicationFactory(thumbnail__filename="tester.jpg")
        self.assertEqual(
            pub.thumbnail.url, f"/media/reading/publications/{pub.slug}/tester.jpg"
        )
        self.assertTrue(
            pub.thumbnail.path.endswith, f"/reading/publications/{pub.slug}/tester.jpg"
        )

        # Tidy up:
        pub.thumbnail.delete()

    @override_settings(
        IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY="imagekit.cachefiles.strategies.Optimistic"
    )
    def test_list_thumbnail(self):
        "It should save a correctly-sized thumbnail to the correct location."
        pub = PublicationFactory(thumbnail__filename="tester.jpg")
        self.assertTrue(
            pub.list_thumbnail.url.startswith(
                f"/media/CACHE/images/reading/publications/{pub.slug}/tester/"
            )
        )
        self.assertIn(
            f"/CACHE/images/reading/publications/{pub.slug}/tester/",
            pub.list_thumbnail.path,
        )
        self.assertEqual(pub.list_thumbnail.width, 80)
        self.assertEqual(pub.list_thumbnail.height, 80)

        # Tidy up:
        pub.thumbnail.delete()

    @override_settings(
        IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY="imagekit.cachefiles.strategies.Optimistic"
    )
    def test_list_thumbnail_2x(self):
        "It should save a correctly-sized thumbnail to the correct location."
        pub = PublicationFactory(thumbnail__filename="tester.jpg")
        self.assertTrue(
            pub.list_thumbnail_2x.url.startswith(
                f"/media/CACHE/images/reading/publications/{pub.slug}/tester/"
            )
        )
        self.assertIn(
            f"/CACHE/images/reading/publications/{pub.slug}/tester/",
            pub.list_thumbnail_2x.path,
        )
        self.assertEqual(pub.list_thumbnail_2x.width, 160)
        self.assertEqual(pub.list_thumbnail_2x.height, 160)

        # Tidy up:
        pub.thumbnail.delete()

    @override_settings(
        IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY="imagekit.cachefiles.strategies.Optimistic"
    )
    def test_detail_thumbnail(self):
        "It should save a correctly-sized thumbnail to the correct location."
        pub = PublicationFactory(thumbnail__filename="tester.jpg")
        self.assertTrue(
            pub.detail_thumbnail.url.startswith(
                f"/media/CACHE/images/reading/publications/{pub.slug}/tester/"
            )
        )
        self.assertIn(
            f"/CACHE/images/reading/publications/{pub.slug}/tester/",
            pub.detail_thumbnail.path,
        )
        self.assertEqual(pub.detail_thumbnail.width, 320)
        self.assertEqual(pub.detail_thumbnail.height, 320)

        # Tidy up:
        pub.thumbnail.delete()

    @override_settings(
        IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY="imagekit.cachefiles.strategies.Optimistic"
    )
    def test_detail_thumbnail_2x(self):
        "It should save a correctly-sized thumbnail to the correct location."
        pub = PublicationFactory(thumbnail__filename="tester.jpg")
        self.assertTrue(
            pub.detail_thumbnail_2x.url.startswith(
                f"/media/CACHE/images/reading/publications/{pub.slug}/tester/"
            )
        )
        self.assertIn(
            f"/CACHE/images/reading/publications/{pub.slug}/tester/",
            pub.detail_thumbnail_2x.path,
        )
        self.assertEqual(pub.detail_thumbnail_2x.width, 640)
        self.assertEqual(pub.detail_thumbnail_2x.height, 640)

        # Tidy up:
        pub.thumbnail.delete()

    def test_exif_data_removed_from_added_thumbnail(self):
        """An image with GPS EXIF data should have it stripped out with a new object.
        Testing the image when added to a brand new publication.
        """

        # The image that has GPS data:
        path = "tests/core/fixtures/images/tester_exif_gps.jpg"

        # Double-check the original image does have some GPS data:
        exif_dict = piexif.load(path)
        self.assertEqual(len(exif_dict["GPS"].keys()), 15)

        pub = PublicationFactory(thumbnail__from_path=path)

        exif_dict = piexif.load(pub.thumbnail.path)
        self.assertEqual(exif_dict["GPS"], {})

        # Tidy up:
        pub.thumbnail.delete()

    def test_exif_data_removed_from_updated_thumbnail(self):
        """A replacement thumbnail should have its GPS data removed.
        i.e. an image that's added to an existing publication, not a brand new one.
        """

        # The image that has GPS data:
        path = "tests/core/fixtures/images/tester_exif_gps.jpg"

        # Double-check it does have some GPS data:
        exif_dict = piexif.load(path)
        self.assertEqual(len(exif_dict["GPS"].keys()), 15)

        # Add an initial image that nas no GPS data:
        pub = PublicationFactory(thumbnail__filename="tester.jpg")
        # Double-check that:
        exif_dict = piexif.load(pub.thumbnail.path)
        self.assertEqual(exif_dict["GPS"], {})

        # Save the path so we can delete the file at the end:
        old_thumbnail_path = pub.thumbnail.path

        # Change the thumbnail to the one with GPS EXIF data:
        with open(path, "rb") as f:
            pub.thumbnail.save(os.path.basename(path), File(f))

        pub.refresh_from_db()

        # Check it does have the new image that had GPS data:
        self.assertEqual(os.path.basename(pub.thumbnail.name), os.path.basename(path))

        # Check the GPS data has now gone:
        exif_dict = piexif.load(pub.thumbnail.path)
        self.assertEqual(exif_dict["GPS"], {})

        # Tidy up:
        pub.thumbnail.delete()
        os.remove(old_thumbnail_path)

    def test_roles(self):
        "It can have multiple PublicationRoles."
        bob = IndividualCreatorFactory(name="Bob")
        terry = IndividualCreatorFactory(name="Terry")
        pub = PublicationFactory()
        bobs_role = PublicationRoleFactory(
            publication=pub, creator=bob, role_name="Editor", role_order=2
        )
        terrys_role = PublicationRoleFactory(
            publication=pub, creator=terry, role_name="Author", role_order=1
        )
        roles = pub.roles.all()
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0], terrys_role)
        self.assertEqual(roles[1], bobs_role)
        self.assertEqual(roles[0].role_name, "Author")
        self.assertEqual(roles[1].role_name, "Editor")

    def test_amazon_uk_url(self):
        p = PublicationFactory(isbn_uk="0356500489")
        self.assertEqual(
            p.amazon_uk_url, "https://www.amazon.co.uk/gp/product/0356500489/"
        )

    def test_amazon_uk_url_none(self):
        p = PublicationFactory(isbn_uk="")
        self.assertEqual(p.amazon_uk_url, "")

    @override_settings(SPECTATOR_AMAZON={"uk": "foobar-21"})
    def test_amazon_uk_url_affiliate(self):
        p = PublicationFactory(isbn_uk="0356500489")
        self.assertEqual(
            p.amazon_uk_url,
            "https://www.amazon.co.uk/gp/product/0356500489/?tag=foobar-21",
        )

    def test_amazon_us_url(self):
        p = PublicationFactory(isbn_us="0356500489")
        self.assertEqual(p.amazon_us_url, "https://www.amazon.com/dp/0356500489/")

    def test_amazon_us_url_none(self):
        p = PublicationFactory(isbn_us="")
        self.assertEqual(p.amazon_us_url, "")

    @override_settings(SPECTATOR_AMAZON={"us": "foobar-20"})
    def test_amazon_us_url_affiliate(self):
        p = PublicationFactory(isbn_us="0356500489")
        self.assertEqual(
            p.amazon_us_url, "https://www.amazon.com/dp/0356500489/?tag=foobar-20"
        )

    def test_amazon_urls(self):
        p = PublicationFactory(isbn_uk="1234567890", isbn_us="3333333333")
        self.assertEqual(
            p.amazon_urls,
            [
                {"url": p.amazon_uk_url, "name": "Amazon.co.uk", "country": "UK"},
                {"url": p.amazon_us_url, "name": "Amazon.com", "country": "USA"},
            ],
        )

    def test_amazon_urls_none(self):
        p = PublicationFactory(isbn_uk="", isbn_us="")
        self.assertEqual(p.amazon_urls, [])

    def test_has_urls_no(self):
        p = PublicationFactory()
        self.assertFalse(p.has_urls)

    def test_has_urls_official(self):
        p = PublicationFactory(official_url="http://www.example.org")
        self.assertTrue(p.has_urls)

    def test_has_urls_notes(self):
        p = PublicationFactory(notes_url="http://www.example.org")
        self.assertTrue(p.has_urls)

    def test_has_urls_isbn_uk(self):
        p = PublicationFactory(isbn_uk="1234567890")
        self.assertTrue(p.has_urls)

    def test_has_urls_isbn_us(self):
        p = PublicationFactory(isbn_us="1234567890")
        self.assertTrue(p.has_urls)

    def test_get_current_reading(self):
        "It should return the one in-progress Reading."
        p = PublicationFactory()
        in_progress = ReadingFactory(publication=p, start_date=make_date("2017-02-15"))
        ReadingFactory(
            publication=p,
            start_date=make_date("2017-02-15"),
            end_date=make_date("2017-02-28"),
        )
        self.assertEqual(p.get_current_reading(), in_progress)

    def test_get_current_reading_none(self):
        "If there's no in-progress Reading, it should return nothing."
        p = PublicationFactory()
        ReadingFactory(
            publication=p,
            start_date=make_date("2017-02-15"),
            end_date=make_date("2017-02-28"),
        )
        self.assertIsNone(p.get_current_reading())


class ReadingTestCase(TestCase):
    def test_str(self):
        reading = ReadingFactory(
            publication=PublicationFactory(title="Big Book"),
            start_date=make_date("2017-02-15"),
            end_date=make_date("2017-02-28"),
        )
        self.assertEqual(str(reading), "Big Book (2017-02-15 to 2017-02-28)")

    def test_clean_error(self):
        "It won't accept an end_date before a start_date."
        reading = ReadingFactory(
            start_date=make_date("2017-02-15"), end_date=make_date("2016-02-28")
        )
        with self.assertRaises(ValidationError):
            reading.clean()

    def test_clean_no_error(self):
        reading = ReadingFactory(
            start_date=make_date("2016-02-28"), end_date=make_date("2017-02-15")
        )
        try:
            reading.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly.")
