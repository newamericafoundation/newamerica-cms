from wagtail.tests.utils import WagtailPageTests
from wagtail.core.models import Page

from home.models import HomePage, PostProgramRelationship

from programs.models import Program, Subprogram, Project

from .models import Quoted, AllQuotedHomePage, ProgramQuotedPage


class QuotedTests(WagtailPageTests):
    """
    Testing the Quoted, AllQuotedHomePage, and
    ProgramQuotedPage models to confirm
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
        self.all_quoted_home_page = self.home_page.add_child(
            instance=AllQuotedHomePage(title='New America In The News')
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
        self.program_quoted_page = self.program_page_1\
            .add_child(instance=ProgramQuotedPage(
                title='OTI In The News')
            )
        self.quoted = Quoted(
            title='Quoted 1',
            slug='quoted-1',
            date='2016-02-10',
            depth=5
        )
        self.program_quoted_page.add_child(
            instance=self.quoted)
        self.quoted.save()


    # Test that a child Page can be created under the appropriate
    # Parent Page
    def test_can_create_quoted_under_program_quoted_page(self):
        self.assertCanCreateAt(ProgramQuotedPage, Quoted)

    def test_can_create_program_quoted_page_under_program(self):
        self.assertCanCreateAt(Program, ProgramQuotedPage)

    def test_can_create_program_quoted_page_under_subprogram(self):
        self.assertCanCreateAt(Subprogram, ProgramQuotedPage)

     # Test allowed parent Page types
    def test_quoted_parent_page(self):
        self.assertAllowedParentPageTypes(
            Quoted, {
                ProgramQuotedPage
            }
        )

    def test_program_quoted_parent_page(self):
        self.assertAllowedParentPageTypes(
            ProgramQuotedPage,
            {Program, Subprogram, Project}
        )

    def test_all_quoted_parent_page(self):
        self.assertAllowedParentPageTypes(
            AllQuotedHomePage,
            {HomePage}
        )

    # Test allowed subpage types
    def test_quoted_subpages(self):
        self.assertAllowedSubpageTypes(Quoted, {})

    def test_program_quoted_subpages(self):
        self.assertAllowedSubpageTypes(ProgramQuotedPage, {Quoted})

    # Test that pages can be created with POST data
    def test_can_create_all_quoted_page_under_homepage(self):
        self.assertCanCreate(self.home_page, AllQuotedHomePage, {
            'title': 'New America In The News Again',
            }
        )

    def test_can_create_program_quoted_page(self):
        self.assertCanCreate(self.program_page_1, ProgramQuotedPage, {
            'title': 'Our Program In The News',
            }
        )

    # Test relationship between quoted and one Program
    def test_quoted_has_relationship_to_one_program(self):
        quoted = Quoted.objects.first()
        self.assertEqual(quoted.parent_programs.all()[0].title, 'OTI')

    # Test you can create a quoted item with two parent Programs
    def test_quoted_has_relationship_to_two_parent_programs(self):
        quoted = Quoted.objects.first()
        relationship, created = PostProgramRelationship.objects.get_or_create(
            program=self.second_program, post=quoted)
        relationship.save()
        self.assertEqual(
            quoted.parent_programs.filter(
                title='Education').first().title, 'Education'
        )

    # Test quoted page with one parent Program can be deleted
    def test_quoted_with_one_parent_program_can_be_deleted(self):
        quoted = Quoted.objects.filter(
            title='Quoted 1').first()
        quoted.delete()
        self.assertEqual(Quoted.objects.filter(
            title='Quoted 1').first(), None
        )
        self.assertNotIn(
            quoted,
            ProgramQuotedPage.objects.filter(
                title='OTI In The News').first().get_children()
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=quoted).first(), None
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=quoted,
                program=self.program_page_1).first(),
            None
        )

    # Test Quoted page with two parent Programs can be deleted
    def test_quoted_with_two_parent_programs_can_be_deleted(self):
        quoted = Quoted.objects.filter(
            title='Quoted 1').first()
        relationship, created = PostProgramRelationship.objects.get_or_create(
            program=self.second_program,
            post=quoted
            )
        if created:
            relationship.save()
        quoted.delete()
        self.assertEqual(Quoted.objects.filter(
            title='Quoted 1').first(), None
        )
        self.assertNotIn(
            quoted,
            ProgramQuotedPage.objects.filter(
                title='OTI In The News').first().get_children()
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=quoted,
                program=self.program_page_1).first(),
            None
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=quoted,
                program=self.second_program).first(), None
        )
