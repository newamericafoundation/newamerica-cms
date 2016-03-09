from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page

from .models import Issue, ProgramIssuesPage

from home.models import HomePage, PostProgramRelationship

from programs.models import Program


class IssueTests(WagtailPageTests):
    """
    Testing the Issue and Program Issues Page
    to confirm hierarchies between pages and
    whether it is possible to create pages
    where appropriate.
    """

    def setUp(self):
        self.login()
        self.root_page = Page.objects.get(id=1)
        self.home_page = self.root_page.add_child(
            instance=HomePage(title='New America')
        )
        self.program_page_1 = self.home_page.add_child(
            instance=Program(title='OTI', name='OTI', location=False, depth=3)
        )
        self.program_issues_page = self.program_page_1.add_child(
            instance=ProgramIssuesPage(title='OTI Issues Page')
        )
        self.issue = self.program_issues_page.add_child(
            instance=Issue(title='Access to Internet', date='2016-03-08')
        )

    # Test that a child Page can be created under
    # the appropriate parent Page
    def test_can_create_program_issues_page_under_program(self):
        self.assertCanCreateAt(Program, ProgramIssuesPage)

    def test_can_create_issue_under_program_issues_page(self):
        self.assertCanCreateAt(ProgramIssuesPage, Issue)

    # Test allowed parent page types
    def test_issue_parent_page(self):
        self.assertAllowedParentPageTypes(
            Issue, {ProgramIssuesPage, Issue}
        )

    def test_program_issues_page(self):
        self.assertAllowedParentPageTypes(
            ProgramIssuesPage, {Program}
        )

    # Test allowed subpage types
    def test_issue_subpages(self):
        self.assertAllowedSubpageTypes(Issue, {Issue})

    def test_program_issue_pages_subpages(self):
        self.assertAllowedSubpageTypes(ProgramIssuesPage, {Issue})

    # Test pages can be created with POST data
    def test_can_create_program_issues_page_under_program_with_data(self):
        self.assertCanCreate(self.program_page_1, ProgramIssuesPage, {
            'title': 'New Issues Homepage for OTI',
            })

    # Test relationship between Issue and Program Issues page
    def test_issue_has_relationship_to_program_issues_page(self):
        issue = Issue.objects.filter(title='Access to Internet')
        self.assertTrue(issue.child_of(self.program_issues_page))

    # Test relationship between Issue and one program
    def test_issue_has_relationship_to_one_program(self):
        issue = Issue.objects.first()
        self.assertEqual(issue.parent_programs.all()[0].title, 'OTI')

    # Test relationship between Issue and two parent Programs
    def test_issue_has_relationship_to_two_programs(self):
        issue = Issue.objects.first()
        program_page_2 = Program.objects.create(
            title='Education',
            name='Education',
            location='False',
            depth=3
        )
        relationship, created = PostProgramRelationship.objects.get_or_create(
            program=program_page_2,
            post=issue
        )
        relationship.save()
        self.assertEqual(issue.parent_programs.filter(
            title='Education').first().title, 'Education'
        )

    # Test Issue page with one parent Program can be deleted
    def test_issue_with_one_parent_program_can_be_deleted(self):
        issue = Issue.objects.filter(title='Access to Internet').first()
        issue.delete()
        self.assertEqual(Issue.objects.filter(
            title='Access to Internet').first(), None
        )
        self.assertNotIn(
            issue,
            ProgramIssuesPage.objects.filter(
                title='OTI Issues Page').first().get_children()
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=issue).first(), None
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=issue,
                program=self.program_page_1).first(),
            None
        )

    # Test Issue page with two parent Programs can be deleted
    def test_issue_with_two_parent_programs_can_be_deleted(self):
        issue = Issue.objects.filter(title='Access to Internet').first()
        program_page_2 = Program.objects.create(
            title='Education',
            name='Education',
            location='False',
            depth=3
        )
        relationship, created = PostProgramRelationship.objects.get_or_create(
            program=program_page_2,
            post=issue
            )
        if created:
            relationship.save()
        issue.delete()
        self.assertEqual(Issue.objects.filter(
            title='Access to Internet').first(), None
        )
        self.assertNotIn(
            issue,
            ProgramIssuesPage.objects.filter(
                title='OTI Issues Page').first().get_children()
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=issue,
                program=self.program_page_1).first(),
            None
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=issue,
                program=program_page_2).first(), None
        )
