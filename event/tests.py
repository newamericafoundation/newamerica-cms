from django.test import TestCase
from datetime import date, timedelta
from django.test import Client

from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page, Site

from .models import Event, AllEventsHomePage, ProgramEventsPage

from home.models import HomePage, PostProgramRelationship

from programs.models import Program, Subprogram


class EventPageViewTests(WagtailPageTests):
    """
    Testing the split views for past
    and future Event pages. Includes tests for
    all event page, and program/subprogram
    event pages.

    """
    def setUp(self):
        self.login()
        site = Site.objects.get()
        page = Page.get_first_root_node()
        home = HomePage(title='New America')
        home_page = page.add_child(instance=home)

        site.root_page = home
        site.save()

        all_events_home_page = home_page.add_child(
            instance=AllEventsHomePage(title="Events")
        )
        program_page_1 = home_page.add_child(
            instance=Program(
                title='OTI',
                name='OTI',
                slug='oti',
                description='OTI',
                location=False,
                depth=3
            )
        )
        program_page_1.save()
        second_program = home_page.add_child(
            instance=Program(
            title='Education',
            name='Education',
            slug='education',
            description='Education',
            location=False,
            depth=3
            )
        )
        second_program.save()
        program_events_page = program_page_1.add_child(
            instance=ProgramEventsPage(title='OTI Events', slug='oti-events')
        )
        program_events_page.save()
        second_program_events_page = second_program.add_child(
            instance=ProgramEventsPage(title='Education Events', slug='education-events')
        )
        second_program_events_page.save()
        today_event = program_events_page.add_child(
            instance=Event(
                title='Today Event' ,
                date=str(date.today()),
                rsvp_link='http://www.newamerica.org',
                soundcloud_url='http://www.newamerica.org'

            )
        )
        today_event.save()
        future_event = program_events_page.add_child(
            instance=Event(
                title='Future Event' ,
                date=str(date.today()+timedelta(days=5)),
                rsvp_link='http://www.newamerica.org',
                soundcloud_url='http://www.newamerica.org'

            )
        )
        future_event.save()
        past_event = program_events_page.add_child(
            instance=Event(
                title='Past Event',
                date=str(date.today()-timedelta(days=5)),
                rsvp_link='http://www.newamerica.org',
                soundcloud_url='http://www.newamerica.org'

            )
        )
        past_event.save()

        second_today_event = second_program_events_page.add_child(
            instance=Event(
                title='Today Event' ,
                date=str(date.today()),
                rsvp_link='http://www.newamerica.org',
                soundcloud_url='http://www.newamerica.org'

            )
        )
        second_today_event.save()
        second_future_event = second_program_events_page.add_child(
            instance=Event(
                title='Future Event' ,
                date=str(date.today()+timedelta(days=5)),
                rsvp_link='http://www.newamerica.org',
                soundcloud_url='http://www.newamerica.org'

            )
        )
        second_future_event.save()
        second_past_event = second_program_events_page.add_child(
            instance=Event(
                title='Past Event',
                date=str(date.today()-timedelta(days=5)),
                rsvp_link='http://www.newamerica.org',
                soundcloud_url='http://www.newamerica.org'

            )
        )
        second_past_event.save()

    # Testing that current day's event and future events
    # show up on the main events page for the program
    def test_program_events_page(self):
        c = Client()
        response = c.get('/oti/oti-events/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['all_events']), 2)

    # Testing past events show up on /past route for program events page
    def test_past_program_events_page(self):
        c = Client()
        response = c.get('/oti/oti-events/past', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['all_events']), 1)


    # Testing that current day's event and future events
    # show up on the org wide events page
    def test_org_wide_events_page(self):
        c = Client()
        response = c.get('/events/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['all_events']), 4)

    # Testing past events show up on /past route for program events page
    def test_org_wide_past_events_page(self):
        c = Client()
        response = c.get('/events/past/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['all_events']), 2)


class EventTests(WagtailPageTests):
    """
    Testing the Event, AllEventsHomePage, and
    ProgramEventsPage models to confirm
    hierarchies between pages and
    whether it is possible to create
    pages where it is appropriate.

    """

    def setUp(self):
        self.login()
        self.root_page = Page.objects.get(id=1)
        self.home_page = self.root_page.add_child(instance=HomePage(
            title='New America')
        )
        self.all_events_home_page = self.home_page.add_child(
            instance=AllEventsHomePage(title="All Events at New America!")
        )
        self.program_page_1 = self.home_page.add_child(
            instance=Program(
                title='OTI',
                name='OTI',
                description='OTI',
                location=False,
                depth=3
            )
        )
        self.second_program = self.home_page.add_child(
            instance=Program(
            title='Education',
            name='Education',
            slug='education',
            description='Education',
            location=False,
            depth=3
            )
        )
        self.program_events_page = self.program_page_1.add_child(
            instance=ProgramEventsPage(title='OTI Events')
        )
        self.event = self.program_events_page.add_child(
            instance=Event(
                title='Event 1',
                date='2016-02-10',
                rsvp_link='http://www.newamerica.org',
                soundcloud_url='http://www.newamerica.org'

            )
        )

    # Test that a child Page can be created under
    # the appropriate parent Page
    def test_can_create_event_under_program_events_page(self):
        self.assertCanCreateAt(ProgramEventsPage, Event)


    def test_can_create_program_events_page_under_program(self):
        self.assertCanCreateAt(Program, ProgramEventsPage)

    # Test allowed parent page types
    def test_event_parent_page(self):
        self.assertAllowedParentPageTypes(
            Event, {ProgramEventsPage}
        )

    def test_program_event_parent_page(self):
        self.assertAllowedParentPageTypes(ProgramEventsPage, {Program, Subprogram})

    def test_all_events_parent_page(self):
        self.assertAllowedParentPageTypes(AllEventsHomePage, {HomePage})

    # Test allowed subpage types
    def test_event_subpages(self):
        self.assertAllowedSubpageTypes(Event, {})

    def test_program_event_subpages(self):
        self.assertAllowedSubpageTypes(ProgramEventsPage, {Event})


    # Test that pages can be created with POST data
    def test_can_create_all_event_page_under_homepage(self):
        self.assertCanCreate(self.home_page, AllEventsHomePage, {
            'title': 'All Events at New America2',
            }
        )

    def test_can_create_program_events_page(self):
        self.assertCanCreate(self.program_page_1, ProgramEventsPage, {
            'title': 'Our Program Events2',
            }
        )

    # Test relationship between event and one
    # Program
    def test_event_has_relationship_to_one_program(self):
        event = Event.objects.first()
        self.assertEqual(event.parent_programs.all()[0].title, 'OTI')


    # Test you can create a event with two parent Programs
    def test_event_has_relationship_to_two_parent_programs(self):
        event = Event.objects.first()
        relationship, created = PostProgramRelationship.objects.get_or_create(
            program=self.second_program, post=event)
        relationship.save()
        self.assertEqual(
            event.parent_programs.filter(title='Education').first().title,
            'Education'
        )

    # Test event can be deleted if attached to one Program
    def test_can_delete_event_with_one_program(self):
        event = Event.objects.filter(title='Event 1').first()
        event.delete()
        self.assertEqual(Event.objects.filter(title='Event 1').first(), None)
        self.assertNotIn(event, ProgramEventsPage.objects.filter(
            title='OTI Events').first().get_children())
        self.assertEqual(PostProgramRelationship.objects.filter(
            post=event).first(), None)
        self.assertEqual(PostProgramRelationship.objects.filter(
            post=event, program=self.program_page_1).first(), None)

    # Test event can be deleted if attached to two Programs
    def test_can_delete_event_with_two_programs(self):
        event = Event.objects.filter(title='Event 1').first()
        relationship, created = PostProgramRelationship.objects.get_or_create(
            program=self.second_program, post=event)
        if created:
            relationship.save()
        event.delete()
        self.assertEqual(Event.objects.filter(title='Event 1').first(), None)
        self.assertNotIn(event, ProgramEventsPage.objects.filter(
            title='OTI Events').first().get_children())
        self.assertEqual(PostProgramRelationship.objects.filter(
            post=event, program=self.program_page_1).first(), None)
        self.assertEqual(PostProgramRelationship.objects.filter(
            post=event, program=self.second_program).first(), None)
