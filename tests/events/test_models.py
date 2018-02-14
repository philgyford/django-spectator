from django.core.exceptions import ValidationError
from django.test import TestCase

from .. import make_date
from spectator.core.factories import *
from spectator.events.factories import *
from spectator.events.models import Event, Venue, Work


class EventStrTestCase(TestCase):
    "Only testing the Event.__str__() method."

    def test_str_with_title(self):
        "If event has a title, that should be used."
        band = GroupCreatorFactory(name='Martha')
        event = GigEventFactory(title='Indietracks 2017')
        EventRoleFactory(event=event, creator=band)
        self.assertEqual(str(event), 'Indietracks 2017')

    def test_str_with_no_title_or_creators(self):
        "With no title or creator names, it still has a __str__"
        event = GigEventFactory(title='')
        self.assertEqual(str(event), 'Event #{}'.format(event.pk))

    def test_str_with_no_title_one_creator(self):
        event = GigEventFactory(title='')
        EventRoleFactory(
                event=event,
                creator=GroupCreatorFactory(name='Martha'),
                role_name='Headliner')
        self.assertEqual(str(event), 'Martha')

    def test_str_with_no_title_several_creators(self):
        "If event has no title, creator names should be used."
        event = GigEventFactory(title='')
        EventRoleFactory(
                event=event,
                creator=GroupCreatorFactory(name='Milky Wimpshake'),
                role_name='Headliner', role_order=1)
        EventRoleFactory(
                event=event,
                creator=GroupCreatorFactory(name='The Tuts'),
                role_name='Support', role_order=3)
        EventRoleFactory(
                event=event,
                creator=GroupCreatorFactory(name='Martha'),
                role_name='Support', role_order=2)
        self.assertEqual(str(event), 'Milky Wimpshake, Martha and The Tuts')

    def test_str_with_title(self):
        event = ConcertEventFactory(title='Amazing Concert!')
        self.assertEqual(str(event), 'Amazing Concert!')

    def test_str_with_no_title_one_work(self):
        "With no title and one work, it uses the work's title."
        event = ConcertEventFactory(title='')
        WorkSelectionFactory(event=event,
                                work=ClassicalWorkFactory(title='Work A'))
        self.assertEqual(str(event), 'Work A')

    def test_str_with_no_title_many_works(self):
        "With no title it uses the titles of the classical works."
        event = ConcertEventFactory(title='')
        WorkSelectionFactory(event=event, work=ClassicalWorkFactory(title='Work A'))
        WorkSelectionFactory(event=event, work=ClassicalWorkFactory(title='Work B'))
        WorkSelectionFactory(event=event, work=ClassicalWorkFactory(title='Work C'))
        self.assertEqual(str(event), 'Work A, Work B and Work C')

    def test_str_with_no_title_and_no_works(self):
        "With no title or works it uses the default."
        event = ConcertEventFactory(title='', pk=5)
        self.assertEqual(str(event), 'Event #5')

    def test_selection_str(self):
        event = ConcertEventFactory(title='My Event')
        selection = WorkSelectionFactory(event=event,
                                    work=ClassicalWorkFactory(title='My Work'))
        self.assertEqual(str(selection), 'Event #{}: My Work'.format(event.pk))


class EventTestCase(TestCase):
    "Testing everything except the __str__() method."

    def test_title_sort_with_no_title(self):
        "If there's no title, title_sort should be based on creators."
        event = GigEventFactory(title='')
        role1 = EventRoleFactory(
                event=event,
                creator=GroupCreatorFactory(name='Milky Wimpshake'),
                role_order=1)
        role2 = EventRoleFactory(
                event=event,
                creator=GroupCreatorFactory(name='Martha'),
                role_order=2)

        event.refresh_from_db()
        self.assertEqual(event.title_sort, 'milky wimpshake and martha')

        # And check it updates after deleting a relationship:
        role2.delete()
        event.refresh_from_db()
        self.assertEqual(event.title_sort, 'milky wimpshake')

    def test_slug(self):
        event = GigEventFactory(pk=123)
        self.assertEqual(event.slug, '9g5o8')

    def test_get_kinds(self):
        self.assertEqual(
            Event.get_kinds(),
            ['movie', 'concert', 'comedy', 'dance', 'exhibition', 'gig',
            'misc', 'play',]
        )

    def test_valid_kind_slugs(self):
        self.assertEqual(
            sorted(Event.get_valid_kind_slugs()),
            sorted(
                ['comedy', 'concerts', 'dance', 'exhibitions', 'gigs', 'misc',
                    'cinema', 'theatre',]
            )
        )

    def test_kind_slug(self):
        "Should be set on save."
        self.assertEqual(ComedyEventFactory().kind_slug, 'comedy')
        self.assertEqual(ConcertEventFactory().kind_slug, 'concerts')
        self.assertEqual(DanceEventFactory().kind_slug, 'dance')
        self.assertEqual(ExhibitionEventFactory().kind_slug, 'exhibitions')
        self.assertEqual(GigEventFactory().kind_slug, 'gigs')
        self.assertEqual(MiscEventFactory().kind_slug, 'misc')
        self.assertEqual(MovieEventFactory().kind_slug, 'cinema')
        self.assertEqual(PlayEventFactory().kind_slug, 'theatre')

    def test_venue_name_set_a_venue(self):
        "If there's a venue, venue_name should be set."
        event = MovieEventFactory(venue=VenueFactory(name='My Venue'))
        self.assertEqual(event.venue_name, 'My Venue')

    def test_venue_name_set_no_venue(self):
        "If there's no venue, venue_name should be empty."
        event = MovieEventFactory(venue=None)
        self.assertEqual(event.venue_name, '')

    def test_venue_name_manually_set(self):
        "If a venue_name is specified it shouldn't be changed by the venue."
        event = MovieEventFactory(
                    venue=VenueFactory(name='My Venue'),
                    venue_name='My Custom Name')
        self.assertEqual(event.venue_name, 'My Custom Name')

    def test_venue_name_remove_venue(self):
        "If the venue is removed, venue_name should be unset."
        event = MovieEventFactory(venue=VenueFactory(name='My Venue'))
        event.venue = None
        event.save()
        self.assertEqual(event.venue_name, '')

    def test_venue_name_change_venue(self):
        "If the venue is changed, venue_name should remain as it was."
        event = MovieEventFactory(venue=VenueFactory(name='Venue 1'))
        event.venue = VenueFactory(name='Venue 2')
        event.save()
        self.assertEqual(event.venue_name, 'Venue 1')

    def test_kind_name(self):
        self.assertEqual(ComedyEventFactory().kind_name, 'Comedy')
        self.assertEqual(ConcertEventFactory().kind_name, 'Concert')
        self.assertEqual(DanceEventFactory().kind_name, 'Dance')
        self.assertEqual(ExhibitionEventFactory().kind_name, 'Exhibition')
        self.assertEqual(GigEventFactory().kind_name, 'Gig')
        self.assertEqual(MiscEventFactory().kind_name, 'Other')
        self.assertEqual(MovieEventFactory().kind_name, 'Cinema')
        self.assertEqual(PlayEventFactory().kind_name, 'Theatre')

    def test_kind_name_plural(self):
        self.assertEqual(ComedyEventFactory().kind_name_plural, 'Comedy')
        self.assertEqual(ConcertEventFactory().kind_name_plural, 'Concerts')
        self.assertEqual(DanceEventFactory().kind_name_plural, 'Dance')
        self.assertEqual(ExhibitionEventFactory().kind_name_plural,
                                                                'Exhibitions')
        self.assertEqual(GigEventFactory().kind_name_plural, 'Gigs')
        self.assertEqual(MiscEventFactory().kind_name_plural, 'Others')
        self.assertEqual(MovieEventFactory().kind_name_plural, 'Cinema')
        self.assertEqual(PlayEventFactory().kind_name_plural, 'Theatre')

    def test_get_kinds_data(self):
        # Not exhaustively testing every part of the data returned...
        data = Event.get_kinds_data()
        self.assertEqual(len(data), 8)
        self.assertEqual(data['gig']['name'], 'Gig')
        self.assertEqual(data['gig']['slug'], 'gigs')
        self.assertEqual(data['gig']['name_plural'], 'Gigs')

    def test_ordering(self):
        "Should order by -date by default."
        e2 = GigEventFactory(title='Event', date=make_date('2017-02-01'))
        e3 = GigEventFactory(title='Abba Event', date=make_date('2017-01-01'))
        e1 = GigEventFactory(title='The Big Event',
                                                date=make_date('2017-03-01'))
        events = Event.objects.all()
        self.assertEqual(events[0], e1)
        self.assertEqual(events[1], e2)
        self.assertEqual(events[2], e3)

    def test_title_sort_ordering(self):
        "Should order by title_sort"
        e3 = GigEventFactory(title='Event')
        e1 = GigEventFactory(title='Abba Event')
        e2 = GigEventFactory(title='The Big Event')
        events = Event.objects.all().order_by('title_sort')
        self.assertEqual(events[0], e1)
        self.assertEqual(events[1], e2)
        self.assertEqual(events[2], e3)

    def test_roles(self):
        "It can have multiple EventRoles."
        bob = IndividualCreatorFactory(name='Bob')
        martha = GroupCreatorFactory(name='Martha')
        event = GigEventFactory()
        bobs_role = EventRoleFactory(event=event, creator=bob,
                                        role_name='Supporter', role_order=2)
        marthas_role = EventRoleFactory(event=event, creator=martha,
                                        role_name='Headliner', role_order=1)
        roles = event.roles.all()
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0], marthas_role)
        self.assertEqual(roles[1], bobs_role)
        self.assertEqual(roles[0].role_name, 'Headliner')
        self.assertEqual(roles[1].role_name, 'Supporter')

    def test_absolute_url_comedy(self):
        event = ComedyEventFactory(pk=123)
        self.assertEqual(event.get_absolute_url(), '/events/9g5o8/')

    def test_absolute_url_concert(self):
        event = ConcertEventFactory(pk=123)
        self.assertEqual(event.get_absolute_url(), '/events/9g5o8/')

    def test_absolute_url_dance(self):
        event = DanceEventFactory(pk=123)
        self.assertEqual(event.get_absolute_url(), '/events/9g5o8/')

    def test_absolute_url_exhibition(self):
        event = ExhibitionEventFactory(pk=123)
        self.assertEqual(event.get_absolute_url(), '/events/9g5o8/')

    def test_absolute_url_gig(self):
        event = GigEventFactory(pk=123)
        self.assertEqual(event.get_absolute_url(), '/events/9g5o8/')

    def test_absolute_url_misc(self):
        event = MiscEventFactory(pk=123)
        self.assertEqual(event.get_absolute_url(), '/events/9g5o8/')

    def test_absolute_url_movie(self):
        event = MovieEventFactory(pk=123)
        self.assertEqual(event.get_absolute_url(), '/events/9g5o8/')

    def test_absolute_url_play(self):
        event = PlayEventFactory(pk=123)
        self.assertEqual(event.get_absolute_url(), '/events/9g5o8/')

    def test_get_works(self):
        event = MovieEventFactory()
        m = MovieFactory()
        p = PlayFactory()
        cw = ClassicalWorkFactory()
        dp = DancePieceFactory()
        WorkSelectionFactory(work=m, event=event, order=4)
        WorkSelectionFactory(work=p, event=event, order=1)
        WorkSelectionFactory(work=cw, event=event, order=3)
        WorkSelectionFactory(work=dp, event=event, order=2)

        works = event.get_works()
        self.assertEqual(len(works), 4)
        self.assertEqual(works[0].work, p)
        self.assertEqual(works[1].work, dp)
        self.assertEqual(works[2].work, cw)
        self.assertEqual(works[3].work, m)

    def test_get_classical_works(self):
        event = MovieEventFactory()
        m = MovieFactory()
        cw = ClassicalWorkFactory()
        WorkSelectionFactory(work=m, event=event)
        WorkSelectionFactory(work=cw, event=event)

        works = event.get_classical_works()
        self.assertEqual(len(works), 1)
        self.assertEqual(works[0].work, cw)

    def test_get_dance_pieces(self):
        event = MovieEventFactory()
        m = MovieFactory()
        dp = DancePieceFactory()
        WorkSelectionFactory(work=m, event=event)
        WorkSelectionFactory(work=dp, event=event)

        works = event.get_dance_pieces()
        self.assertEqual(len(works), 1)
        self.assertEqual(works[0].work, dp)

    def test_get_movies(self):
        event = MovieEventFactory()
        m = MovieFactory()
        p = PlayFactory()
        WorkSelectionFactory(work=m, event=event)
        WorkSelectionFactory(work=p, event=event)

        works = event.get_movies()
        self.assertEqual(len(works), 1)
        self.assertEqual(works[0].work, m)

    def test_get_plays(self):
        event = MovieEventFactory()
        m = MovieFactory()
        p = PlayFactory()
        WorkSelectionFactory(work=m, event=event)
        WorkSelectionFactory(work=p, event=event)

        works = event.get_plays()
        self.assertEqual(len(works), 1)
        self.assertEqual(works[0].work, p)


class WorkTestCase(TestCase):

    def test_ordering(self):
        w3 = MovieFactory(title='C')
        w1 = PlayFactory(title='A')
        w2 = DancePieceFactory(title='B')
        works = Work.objects.all()
        self.assertEqual(works[0], w1)
        self.assertEqual(works[1], w2)
        self.assertEqual(works[2], w3)

    def test_slug(self):
        work = MovieFactory(pk=123)
        self.assertEqual(work.slug, '9g5o8')

    def test_roles(self):
        "It can have multiple WorkRoles."
        bob = IndividualCreatorFactory(name='Bob')
        terry = IndividualCreatorFactory(name='Terry')
        work = MovieFactory()
        bobs_role = WorkRoleFactory(work=work, creator=bob,
                                        role_name='Actor', role_order=2)
        terrys_role = WorkRoleFactory(work=work, creator=terry,
                                        role_name='Director', role_order=1)
        roles = work.roles.all()
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0], terrys_role)
        self.assertEqual(roles[1], bobs_role)
        self.assertEqual(roles[0].role_name, 'Director')
        self.assertEqual(roles[1].role_name, 'Actor')

    def test_absolute_url_classicalwork(self):
        work = ClassicalWorkFactory(pk=123)
        self.assertEqual(work.get_absolute_url(), '/events/classical-works/9g5o8/')

    def test_get_list_url_classicalwork(self):
        work = ClassicalWorkFactory()
        self.assertEqual(work.get_list_url(), '/events/classical-works/')

    def test_absolute_url_dancepiece(self):
        work = DancePieceFactory(pk=123)
        self.assertEqual(work.get_absolute_url(), '/events/dance-pieces/9g5o8/')

    def test_get_list_url_dancepiece(self):
        work = DancePieceFactory()
        self.assertEqual(work.get_list_url(), '/events/dance-pieces/')

    def test_absolute_url_movie(self):
        work = MovieFactory(pk=123)
        self.assertEqual(work.get_absolute_url(), '/events/movies/9g5o8/')

    def test_get_list_url_movie(self):
        work = MovieFactory()
        self.assertEqual(work.get_list_url(), '/events/movies/')

    def test_absolute_url_play(self):
        work = PlayFactory(pk=123)
        self.assertEqual(work.get_absolute_url(), '/events/plays/9g5o8/')

    def test_get_list_url_plays(self):
        work = PlayFactory()
        self.assertEqual(work.get_list_url(), '/events/plays/')

    def test_imdb_url_with_id(self):
        work = MovieFactory(imdb_id='tt0056687')
        self.assertEqual(work.imdb_url, 'http://www.imdb.com/title/tt0056687/')

    def test_imdb_url_with_no_id(self):
        work = MovieFactory(imdb_id='')
        self.assertEqual(work.imdb_url, '')


class VenueTestCase(TestCase):

    def test_str(self):
        venue = VenueFactory(name='My Venue')
        self.assertEqual(str(venue), 'My Venue')

    def test_ordering(self):
        "Should order by venue name."
        v3 = VenueFactory(name='Venue C')
        v1 = VenueFactory(name='Venue A')
        v2 = VenueFactory(name='Venue B')
        venues = Venue.objects.all()
        self.assertEqual(venues[0], v1)
        self.assertEqual(venues[1], v2)
        self.assertEqual(venues[2], v3)

    def test_slug(self):
        venue = VenueFactory(pk=123)
        self.assertEqual(venue.slug, '9g5o8')

    def test_absolute_url(self):
        venue = VenueFactory(pk=123)
        self.assertEqual(venue.get_absolute_url(), '/events/venues/9g5o8/')

    def test_country_name_yes(self):
        venue = VenueFactory(country='GB')
        self.assertEqual(venue.country_name, 'UK')

    def test_country_name_no(self):
        venue = VenueFactory(country='')
        self.assertEqual(venue.country_name, None)

    def test_cinema_treasures_url_with_id(self):
        venue = VenueFactory(cinema_treasures_id=1234)
        self.assertEqual(venue.cinema_treasures_url,
                        'http://cinematreasures.org/theaters/1234')

    def test_cinema_treasures_url_no_id(self):
        venue = VenueFactory(cinema_treasures_id=None)
        self.assertEqual(venue.cinema_treasures_url, '')
