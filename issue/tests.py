from django.test import TestCase

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

	def setup(self):
		self.login()
        self.root_page = Page.objects.get(id=1)
        self.home_page = self.root_page.add_child(instance=HomePage(
            title='New America')
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