# coding: utf-8
from django.test import override_settings, TestCase

from spectator.core.factories import *
from spectator.events.factories import *
from spectator.reading.factories import *
from spectator.core.models import Creator


class SluggedModelMixinTestCase(TestCase):
    """
    Using the Creator model to test that SluggedModelMixin works correctly.
    """

    def test_default_alphabet_and_slug(self):
        creator = IndividualCreatorFactory(pk=123)
        self.assertEqual(creator.slug, '9g5o8')

    @override_settings(SPECTATOR_SLUG_ALPHABET='ABCDEFG1234567890')
    def test_custom_alphabet(self):
        creator = IndividualCreatorFactory(pk=123)
        self.assertEqual(creator.slug, '18G28')

    @override_settings(SPECTATOR_SLUG_SALT='My new salt')
    def test_custom_salt(self):
        creator = IndividualCreatorFactory(pk=123)
        self.assertEqual(creator.slug, 'y9xgy')


class CreatorTestCase(TestCase):

    def test_str(self):
        creator = IndividualCreatorFactory(name='Bill Brown')
        self.assertEqual(str(creator), 'Bill Brown')

    def test_ordering(self):
        # Will have a name_sort of 'peaness':
        b = IndividualCreatorFactory(name='Peaness')
        # Will have a name_sort of 'long blondes, the':
        a = IndividualCreatorFactory(name='The Long Blondes')
        creators = Creator.objects.all()
        self.assertEqual(creators[0], a)
        self.assertEqual(creators[1], b)

    def test_slug(self):
        creator = IndividualCreatorFactory(pk=123)
        self.assertEqual(creator.slug, '9g5o8')

    def test_absolute_url(self):
        creator = IndividualCreatorFactory(pk=123)
        self.assertEqual(creator.get_absolute_url(), '/creators/9g5o8/')

    def test_publication_roles(self):
        bob = IndividualCreatorFactory(name='Bob')
        pub1 = PublicationFactory(title='Publication 1')
        pub2 = PublicationFactory(title='Publication 2')
        role1 = PublicationRoleFactory(
                        publication=pub1, creator=bob, role_name='Author')
        role2 = PublicationRoleFactory(
                        publication=pub2, creator=bob, role_name='Editor')
        roles = bob.publication_roles.all()
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0], role1)
        self.assertEqual(roles[1], role2)
        self.assertEqual(roles[0].role_name, 'Author')
        self.assertEqual(roles[1].role_name, 'Editor')

    def test_event_roles(self):
        bob = IndividualCreatorFactory(name='Bob')
        event1 = GigEventFactory()
        event2 = GigEventFactory()
        role1 = EventRoleFactory(
                        event=event1, creator=bob, role_name='Headliner')
        role2 = EventRoleFactory(
                        event=event2, creator=bob, role_name='Support')
        roles = bob.event_roles.all()
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0], role1)
        self.assertEqual(roles[1], role2)
        self.assertEqual(roles[0].role_name, 'Headliner')
        self.assertEqual(roles[1].role_name, 'Support')

    def test_work_roles(self):
        bob = IndividualCreatorFactory()
        movie = MovieFactory()
        play = PlayFactory()
        role1 = WorkRoleFactory(
                        work=movie, creator=bob,
                        role_name='Director', role_order=1)
        role2 = WorkRoleFactory(
                        work=play, creator=bob,
                        role_name='Actor', role_order=2)
        roles = bob.work_roles.all()
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0], role1)
        self.assertEqual(roles[1], role2)
        self.assertEqual(roles[0].role_name, 'Director')
        self.assertEqual(roles[1].role_name, 'Actor')

    def test_get_works(self):
        bob = IndividualCreatorFactory()
        m = MovieFactory()
        p = PlayFactory()
        cw = ClassicalWorkFactory()
        dp = DancePieceFactory()

        WorkRoleFactory(work=m, creator=bob, role_name='Director')
        WorkRoleFactory(work=m, creator=bob, role_name='Actor')
        WorkRoleFactory(work=p, creator=bob)
        WorkRoleFactory(work=cw, creator=bob)
        WorkRoleFactory(work=dp, creator=bob)

        works = bob.get_works()
        self.assertEqual(len(works), 4)

    def test_get_classical_works(self):
        bob = IndividualCreatorFactory()
        m = MovieFactory()
        cw = ClassicalWorkFactory()
        WorkRoleFactory(work=m, creator=bob)
        WorkRoleFactory(work=cw, creator=bob)

        works = bob.get_classical_works()
        self.assertEqual(len(works), 1)
        self.assertEqual(works[0], cw)

    def test_get_dance_pieces(self):
        bob = IndividualCreatorFactory()
        m = MovieFactory()
        dp = DancePieceFactory()
        WorkRoleFactory(work=m, creator=bob)
        WorkRoleFactory(work=dp, creator=bob)

        pieces = bob.get_dance_pieces()
        self.assertEqual(len(pieces), 1)
        self.assertEqual(pieces[0], dp)

    def test_get_movies(self):
        bob = IndividualCreatorFactory()
        m = MovieFactory()
        p = PlayFactory()
        WorkRoleFactory(work=m, creator=bob)
        WorkRoleFactory(work=p, creator=bob)

        movies = bob.get_movies()
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0], m)

    def test_get_plays(self):
        bob = IndividualCreatorFactory()
        m = MovieFactory()
        p = PlayFactory()
        WorkRoleFactory(work=m, creator=bob)
        WorkRoleFactory(work=p, creator=bob)

        plays = bob.get_plays()
        self.assertEqual(len(plays), 1)
        self.assertEqual(plays[0], p)
