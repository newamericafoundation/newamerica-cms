from django.test import TestCase

from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page

from .models import Event, AllEventsHomePage, ProgramEventsPage

from home.models import HomePage, PostProgramRelationship

from programs.models import Program


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
            instance=Program(title='OTI', name='OTI', location=False, depth=3)
        )
        self.program_events_page = self.program_page_1.add_child(
            instance=ProgramEventsPage(title='OTI Events')
        )
        self.event = self.program_events_page.add_child(
            instance=Event(title='Event 1', date='2016-02-10')
        )
        self.org_wide_event = self.all_events_home_page.add_child(
            instance=Event(title="Org Event", date='2016-02-10')
        )

    # Test that a child Page can be created under
    # the appropriate parent Page
    def test_can_create_event_under_program_events_page(self):
        self.assertCanCreateAt(ProgramEventsPage, Event)

    # Test whether events can be created at the
    # org wide level
    def test_can_create_event_under_all_events_page(self):
        self.assertCanCreateAt(AllEventsHomePage, Event)

    def test_can_create_program_events_page_under_program(self):
        self.assertCanCreateAt(Program, ProgramEventsPage)

    # Test allowed parent page types
    def test_event_parent_page(self):
        self.assertAllowedParentPageTypes(
            Event, {ProgramEventsPage, AllEventsHomePage}
        )

    def test_program_event_parent_page(self):
        self.assertAllowedParentPageTypes(ProgramEventsPage, {Program})

    def test_all_events_parent_page(self):
        self.assertAllowedParentPageTypes(AllEventsHomePage, {HomePage})

    # Test allowed subpage types
    def test_blog_post_subpages(self):
        self.assertAllowedSubpageTypes(Event, {})

    def test_program_event_subpages(self):
        self.assertAllowedSubpageTypes(ProgramEventsPage, {Event})

    def test_all_event_subpages(self):
        self.assertAllowedSubpageTypes(AllEventsHomePage, {Event})

    # Test that pages can be created with POST data
    def test_can_create_all_event_page_under_homepage(self):
        self.assertCanCreate(self.home_page, AllEventsHomePage, {
            'title': 'All Events at New America',
            }
        )

    def test_can_create_program_events_page(self):
        self.assertCanCreate(self.program_page_1, ProgramEventsPage, {
            'title': 'Our Program Events',
            }
        )

    # Test relationship between event and one
    # Program
    def test_event_has_relationship_to_one_program(self):
        event = Event.objects.first()
        self.assertEqual(event.parent_programs.all()[0].title, 'OTI')

    # Test relationship between event and all events homepage
    def test_event_has_relationship_to_all_event_homepage(self):
        event = Event.objects.filter(title="Org Event")
        self.assertTrue(event.child_of(self.all_events_home_page))

    # Test you can create a event with two parent Programs
    def test_event_has_relationship_to_two_parent_programs(self):
        event = Event.objects.first()
        second_program = Program.objects.create(
            title='Education', name='Education', location=False, depth=3)
        relationship, created = PostProgramRelationship.objects.get_or_create(
            program=second_program, post=event)
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
        second_program = Program.objects.create(
            title='Education', name='Education', location=False, depth=3)
        relationship, created = PostProgramRelationship.objects.get_or_create(
            program=second_program, post=event)
        if created:
            relationship.save()
        event.delete()
        self.assertEqual(Event.objects.filter(title='Event 1').first(), None)
        self.assertNotIn(event, ProgramEventsPage.objects.filter(
            title='OTI Events').first().get_children())
        self.assertEqual(PostProgramRelationship.objects.filter(
            post=event, program=self.program_page_1).first(), None)
        self.assertEqual(PostProgramRelationship.objects.filter(
            post=event, program=second_program).first(), None)
