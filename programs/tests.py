import io

from django.core import management
from django.test import TestCase
from wagtail.core.models import Page
from wagtail.tests.utils import WagtailPageTests

from article.models import AllArticlesHomePage, Article, ProgramArticlesPage
from blog.models import AllBlogPostsHomePage, ProgramBlogPostsPage
from book.models import AllBooksHomePage, ProgramBooksPage
from event.models import AllEventsHomePage, ProgramEventsPage
from home.models import (
    HomePage, JobsPage, OrgSimplePage, ProgramAboutHomePage, ProgramSimplePage,
    RedirectPage, SubscribePage
)
from issue.models import IssueOrTopic, TopicHomePage
from other_content.models import ProgramOtherPostsPage
from person.models import (
    BoardAndLeadershipPeoplePage, OurPeoplePage, ProgramPeoplePage
)
from podcast.models import AllPodcastsHomePage, ProgramPodcastsPage
from policy_paper.models import (
    AllPolicyPapersHomePage, ProgramPolicyPapersPage
)
from press_release.models import (
    AllPressReleasesHomePage, ProgramPressReleasesPage
)
from quoted.models import AllQuotedHomePage, ProgramQuotedPage
from report.models import ReportsHomepage
from survey.models import SurveysHomePage
from test_factories import PostFactory
from weekly.models import Weekly
from the_thread.models import Thread

from .models import (
    Program, ProgramSubprogramRelationship, Project, PublicationsPage,
    Subprogram
)


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
        self.subprogram_articles_page = self.subprogram_page.add_child(
            instance=ProgramArticlesPage(title='Subprogram Articles')
        )
        self.subprogram_article = self.subprogram_articles_page.add_child(
            instance=Article(
                title='Article 2',
                date='2016-02-03'
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
                ProgramAboutHomePage,
                SurveysHomePage
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
                ProgramAboutHomePage,
                SurveysHomePage
            }
        )


class SearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        cls.program = PostFactory.create_program(
            home_page=home_page,
            program_data={
                'title': 'Robots Program'
            }
        )

        cls.project1 = cls.program.add_child(
            instance=Project(
                title='Cyborg Project',
                name='Cyborg Project',
                description='Secret',
            )
        )

        cls.redirect_project = cls.program.add_child(
            instance=Project(
                title='Cyborg Project',
                name='Cyborg Project',
                description='Secret',
                redirect_page=cls.project1,
            )
        )

    def setUp(self):
        management.call_command('update_index', stdout=io.StringIO(), chunk_size=50)

    def test_program_search_excludes_redirect_projects(self):
        qs = (
            Page.objects
            .live()
            .public()
            .type((Program, Subprogram))
            .search('cyborg', partial_match=False)
        )

        found_pks = {x.pk for x in qs}
        self.assertIn(self.project1.pk, found_pks)
        self.assertNotIn(self.redirect_project.pk, found_pks)
