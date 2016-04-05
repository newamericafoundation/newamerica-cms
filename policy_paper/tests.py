from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page

from django.test import TestCase

from home.models import HomePage, PostProgramRelationship

from programs.models import Program

from .models import PolicyPaper, AllPolicyPapersHomePage, ProgramPolicyPapersPage


class PolicyPaperTests(WagtailPageTests):
    """
    Testing the PolicyPaper, AllPolicyPapersHomePage, and
    ProgramPolicyPapersPage models to confirm
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
        self.all_policy_papers_home_page = self.home_page.add_child(
            instance=AllPolicyPapersHomePage(title='New America Policy Papers')
        )
        self.program_page_1 = self.home_page.add_child(
            instance=Program(title='OTI', name='OTI', location=False, depth=3)
        )
        self.program_policy_papers_page = self.program_page_1.add_child(instance=ProgramPolicyPapersPage(
                title='OTI Policy Papers'))
        
        self.policy_paper = PolicyPaper(title='Policy Paper 1', slug='policy-paper-1', date='2016-02-10', depth=5)

        self.program_policy_papers_page.add_child(
            instance=self.policy_paper)
        
        self.policy_paper.save()

    # Test that a child Page can be created under hte appropriate
    # Parent Page
    def test_can_create_policy_paper_under_program_policy_papers_page(self):
        self.assertCanCreateAt(ProgramPolicyPapersPage, PolicyPaper)

    def test_can_create_program_policy_papers_page_under_program(self):
        self.assertCanCreateAt(ProgramPolicyPapersPage, PolicyPaper)

