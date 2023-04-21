from wagtail.test.utils import WagtailPageTests
from wagtail.models import Page

from .models import IssueOrTopic, TopicHomePage

from home.models import HomePage, PostProgramRelationship

from programs.models import Program, Subprogram


class IssueOrTopicTests(WagtailPageTests):
    """
    Testing the IssueOrTopic model
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
            instance=Program(title='OTI', name='OTI', description='OTI',location=False, depth=3)
        )

    def test_can_create_issue_under_program_issues_page(self):
        self.assertCanCreateAt(Program, IssueOrTopic)

    def test_can_create_issue_under_program_issues_page(self):
        self.assertCanCreateAt(IssueOrTopic, IssueOrTopic)

    # Test allowed parent page types
    def test_issue_parent_page(self):
        self.assertAllowedParentPageTypes(
            IssueOrTopic, {
                TopicHomePage,
                IssueOrTopic
            }
        )

    # Test allowed subpage types
    def test_issue_subpages(self):
        self.assertAllowedSubpageTypes(IssueOrTopic, {
            IssueOrTopic
        })
