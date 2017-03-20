from distutils.version import StrictVersion

from django import get_version
from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from . import make_date
from spectator.admin import PublicationAdmin, PlayAdmin, PlayProductionAdmin,\
        PlayProductionLinkInline
from spectator.factories import PublicationFactory, PublicationRoleFactory,\
        PlayFactory, PlayProductionFactory,\
        PlayProductionEventFactory,\
        PlayProductionRoleFactory, PlayRoleFactory,\
        IndividualCreatorFactory, VenueFactory
from spectator.models import Publication, Play, PlayProduction


class AdminTestCase(TestCase):

    def setUp(self):
        self.site = AdminSite()


class PlayProductionLinkInlineTestCase(AdminTestCase):

    def test_display_str_with_instance(self):
        "It should return the correct string with a saved instance."
        pp = PlayProductionFactory(title='Production Name')
        v1 = VenueFactory(name='Venue 1')
        v2 = VenueFactory(name='Venue 2')
        pp.playproductionevent_set.add(
            PlayProductionEventFactory(venue=v1, date=make_date('2017-02-20')))
        pp.playproductionevent_set.add(
            PlayProductionEventFactory(venue=v2, date=make_date('2016-12-30')))
        ppli = PlayProductionLinkInline(pp, self.site)
        self.assertEqual(
            ppli.display_str(pp),
            "Production Name<br>• 2016-12-30 – Venue 2<br>• 2017-02-20 – Venue 1"
        )

    def test_display_str_with_no_instance(self):
        "It should return the correct string without a saved instance."
        pp = PlayProduction()
        ppli = PlayProductionLinkInline(pp, self.site)
        self.assertEqual(
            ppli.display_str(pp),
            '<a href="/admin/spectator/playproduction/add/" class="js-add-event-link">Add another Play Production and event</a>'
        )

    def test_get_max_num(self):
        "It should return the correct number."
        p = PlayFactory()
        pp1 = PlayProductionFactory()
        pp2 = PlayProductionFactory()
        p.playproduction_set.add(pp1)
        p.playproduction_set.add(pp2)
        ppli = PlayProductionLinkInline(pp1, self.site)
        self.assertEqual(ppli.get_max_num(None, obj=p), 3)

    def test_changeform_link_with_instance(self):
        "It should return the correct string with a saved instance."
        pp = PlayProductionFactory()
        ppli = PlayProductionLinkInline(pp, self.site)
        # change URLs are slightly different for Django < 1.9:
        if StrictVersion(get_version()) < StrictVersion('1.9'):
            self.assertEqual(
                ppli.changeform_link(pp),
                '<a href="/admin/spectator/playproduction/1/">Change production and/or event(s)</a>'
            )
        else:
            self.assertEqual(
                ppli.changeform_link(pp),
                '<a href="/admin/spectator/playproduction/1/change/">Change production and/or event(s)</a>'
            )

    def test_changeform_link_with_no_instance(self):
        "It should return an empty string without a saved instance."
        pp = PlayProduction()
        ppli = PlayProductionLinkInline(pp, self.site)
        self.assertEqual(ppli.changeform_link(pp), '')


class PublicationAdminTestCase(AdminTestCase):

    def test_show_creators_with_roles(self):
        "When a Publication has roles, display them."
        pub = PublicationFactory()
        PublicationRoleFactory(
                publication=pub,
                creator=IndividualCreatorFactory(name='Bob'),
                role_order=1)
        PublicationRoleFactory(
                publication=pub,
                creator=IndividualCreatorFactory(name='Terry'),
                role_order=2)

        ba = PublicationAdmin(Publication, self.site)
        self.assertEqual(ba.show_creators(pub), 'Bob, Terry')

    def test_show_creators_no_roles(self):
        "When a Publication has no roles, display '-'."
        pub = PublicationFactory()

        ba = PublicationAdmin(Publication, self.site)
        self.assertEqual(ba.show_creators(pub), '-')


class PlayAdminTestCase(AdminTestCase):

    def test_show_creators_with_roles(self):
        "When a Play has roles, display them."
        play = PlayFactory()
        PlayRoleFactory(
                play=play,
                creator=IndividualCreatorFactory(name='Bob'),
                role_order=1)
        PlayRoleFactory(
                play=play,
                creator=IndividualCreatorFactory(name='Terry'),
                role_order=2)

        pa = PlayAdmin(Play, self.site)
        self.assertEqual(pa.show_creators(play), 'Bob, Terry')

    def test_show_creators_no_roles(self):
        "When a Play has no roles, display '-'."
        play = PlayFactory()

        pa = PlayAdmin(Play, self.site)
        self.assertEqual(pa.show_creators(play), '-')


class PlayProductionAdminTestCase(AdminTestCase):

    def test_show_creators_with_two_roles(self):
        "When a PlayProduction has roles, display them."
        production = PlayProductionFactory()
        PlayProductionRoleFactory(
                production=production,
                creator=IndividualCreatorFactory(name='Bob'),
                role_order=1)
        PlayProductionRoleFactory(
                production=production,
                creator=IndividualCreatorFactory(name='Terry'),
                role_order=2)

        ppa = PlayProductionAdmin(PlayProduction, self.site)
        self.assertEqual(ppa.show_creators(production), 'Bob, Terry')

    def test_show_creators_with_more_than_three_roles(self):
        "When a PlayProduction has many roles, display one."
        production = PlayProductionFactory()
        PlayProductionRoleFactory(
                production=production,
                creator=IndividualCreatorFactory(name='Bob'),
                role_order=1)
        PlayProductionRoleFactory(
                production=production,
                creator=IndividualCreatorFactory(name='Terry'),
                role_order=2)
        PlayProductionRoleFactory(
                production=production,
                creator=IndividualCreatorFactory(name='Audrey'),
                role_order=3)
        PlayProductionRoleFactory(
                production=production,
                creator=IndividualCreatorFactory(name='Thelma'),
                role_order=4)

        ppa = PlayProductionAdmin(PlayProduction, self.site)
        self.assertEqual(ppa.show_creators(production), 'Bob et al.')

    def test_show_creators_no_roles(self):
        "When a PlayProduction has no roles, display '-'."
        production = PlayProductionFactory()

        ppa = PlayProductionAdmin(PlayProduction, self.site)
        self.assertEqual(ppa.show_creators(production), '-')


