from wagtail.tests.utils import WagtailPageTests
from wagtail.core.models import Page

from home.models import HomePage, OrgSimplePage, ProgramSimplePage, JobsPage, SubscribePage, RedirectPage, ProgramAboutHomePage

from .models import Program, Subprogram, ProgramSubprogramRelationship, PublicationsPage, Project

from weekly.models import Weekly

from article.models import AllArticlesHomePage, ProgramArticlesPage, Article

from event.models import AllEventsHomePage, ProgramEventsPage

from blog.models import AllBlogPostsHomePage, ProgramBlogPostsPage

from book.models import AllBooksHomePage, ProgramBooksPage

from person.models import OurPeoplePage, BoardAndLeadershipPeoplePage, ProgramPeoplePage

from podcast.models import AllPodcastsHomePage, ProgramPodcastsPage

from policy_paper.models import AllPolicyPapersHomePage, ProgramPolicyPapersPage

from press_release.models import AllPressReleasesHomePage, ProgramPressReleasesPage

from quoted.models import AllQuotedHomePage, ProgramQuotedPage

from issue.models import IssueOrTopic, TopicHomePage

from report.models import ReportsHomepage

from other_content.models import ProgramOtherPostsPage

class ProgramsTests(WagtailPageTests):
    """
    Testing hierarchies between pages and whether it is possible
    to create a Program and all the allowed subpages
    underneath Programs and Subprograms.

    Testing functionality of lead, feature, and feature carousels on
    the landing page.

    Also testing for Programs adding items the sidebar menu.
    """

    def setUp(self):
        self.login()
        self.root_page = Page.objects.get(id=1)
        self.home_page = self.root_page.add_child(instance=HomePage(
            title='New America')
        )
        self.program_page = self.home_page.add_child(
            instance=Program(
                title='OTI',
                name='OTI',
                description='OTI',
                location=False,
                depth=3
            )
        )
        self.subprogram_page = self.program_page.add_child(
            instance=Subprogram(
                title='OTI Subprogram',
                name='OTI Subprogram',
                description='OTI Subprogram',
                location=False,
                depth=4,
            )
        )
        self.program_articles_page = self.program_page.add_child(
            instance=ProgramArticlesPage(title='Program Articles')
        )
        self.article = self.program_articles_page.add_child(
            instance=Article(
                title='Article 1',
                date='2016-02-02'
            )
        )

    # Test that a particular child Page type
    # can be created under a parent Page type
    def test_program_parent_page_type(self):
        self.assertCanCreateAt(HomePage, Program)

    def test_subprogram_parent_page_type(self):
        self.assertCanCreateAt(Program, Subprogram)

    def test_subprogram_not_parent_page(self):
        self.assertCanNotCreateAt(HomePage, Subprogram)

    # Test that the only page types that can be created
    # under parent_model are child_models
    def test_program_subpages(self):
        self.assertAllowedSubpageTypes(
            Program,
            {
                ProgramArticlesPage,
                ProgramBooksPage,
                ProgramBlogPostsPage,
                ProgramEventsPage,
                ProgramPodcastsPage,
                ProgramPolicyPapersPage,
                ProgramPressReleasesPage,
                ProgramQuotedPage,
                ProgramSimplePage,
                ProgramPeoplePage,
                Subprogram,
                RedirectPage,
                ReportsHomepage,
                PublicationsPage,
                ProgramOtherPostsPage,
                Project,
                TopicHomePage,
                ProgramAboutHomePage
            }
        )

    def test_subprogram_subpages(self):
        self.assertAllowedSubpageTypes(
            Subprogram,
            {
                ProgramArticlesPage,
                ProgramBooksPage,
                ProgramBlogPostsPage,
                ProgramEventsPage,
                ProgramPodcastsPage,
                ProgramPolicyPapersPage,
                ProgramPressReleasesPage,
                ProgramQuotedPage,
                ProgramSimplePage,
                ProgramPeoplePage,
                RedirectPage,
                PublicationsPage,
                ProgramOtherPostsPage,
                ReportsHomepage,
                ProgramAboutHomePage
            }
        )
