from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page

from .models import Podcast, AllPodcastsHomePage, ProgramPodcastsPage

from home.models import HomePage, PostProgramRelationship

from programs.models import Program


class PodcastTests(WagtailPageTests):
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
        self.all_podcasts_home_page = self.home_page.add_child(
            instance=AllPodcastsHomePage(title="All Podcasts at New America!")
        )
        self.program_page_1 = self.home_page.add_child(
            instance=Program(title='OTI', name='OTI', location=False, depth=3)
        )
        self.program_podcasts_page = self.program_page_1.add_child(
            instance=ProgramPodcastsPage(title='OTI Podcasts')
        )
        self.podcast = self.program_podcasts_page.add_child(
            instance=Podcast(title='Podcast 1', date='2016-02-10')
        )

    # Test that a child Page can be created under
    # the appropriate parent Page
    def test_can_create_podcast_under_program_podcasts_page(self):
        self.assertCanCreateAt(ProgramPodcastsPage, Podcast)

    def test_can_create_program_podcasts_page_under_program(self):
        self.assertCanCreateAt(Program, ProgramPodcastsPage)

    # Test allowed parent page types
    def test_podcast_parent_page(self):
        self.assertAllowedParentPageTypes(
            Podcast, {ProgramPodcastsPage}
        )

    def test_program_podcasts_parent_page(self):
        self.assertAllowedParentPageTypes(ProgramPodcastsPage, {Program})

    def test_all_podcasts_parent_page(self):
        self.assertAllowedParentPageTypes(AllPodcastsHomePage, {HomePage})

    # Test allowed subpage types
    def test_podcast_subpages(self):
        self.assertAllowedSubpageTypes(Podcast, {})

    def test_program_podcast_subpages(self):
        self.assertAllowedSubpageTypes(ProgramPodcastsPage, {Podcast})

    # Test that pages can be created with POST data
    def test_can_create_all_podcasts_page_under_homepage(self):
        self.assertCanCreate(self.home_page, AllPodcastsHomePage, {
            'title': 'All Podcasts at New America',
            }
        )

    def test_can_create_program_podcasts_page(self):
        self.assertCanCreate(self.program_page_1, ProgramPodcastsPage, {
            'title': 'Our Program Podcasts',
            }
        )
