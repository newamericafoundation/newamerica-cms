from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page

from django.test import TestCase

from home.models import HomePage, PostProgramRelationship

from programs.models import Program

from .models import PolicyPaper, AllPolicyPapersHomePage, ProgramPolicyPapersPage


class PolicyPaperTests(WagtailPageTests):
	"""
	Testing the Podcast, AllPodcastsHomePage, and
    ProgramPodcastsPage models to confirm
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
        self.program_policy_papers_page = self.program_page_1.add_child(instance=ProgramPodcastsPage(
                title='OTI Policy Papers'))
        
        self.podcast = self.program_podcasts_page.add_child(
            instance=Podcast(title='Podcast 1', date='2016-02-10')
        )