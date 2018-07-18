from wagtail.tests.utils import WagtailPageTests
from wagtail.core.models import Page

from home.models import HomePage, OrgSimplePage, ProgramSimplePage, JobsPage, SubscribePage, RedirectPage

from .models import Program, Subprogram, ProgramSubprogramRelationship

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

from issue.models import IssueOrTopic


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
                IssueOrTopic,
                RedirectPage,
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
                IssueOrTopic,
                RedirectPage,
            }
        )

    # Test that pages can be created with POST data
    def test_can_create_program_under_homepage(self):
        self.assertCanCreate(self.home_page, Program, {
            'title': 'Test Program 1',
            'name': 'Test Program 1',
            'slug': 'test-program-1',
            'description': 'Test description',
            'depth': 3,
            'location': False,
            'feature_carousel-count': 0,
            'sidebar_menu_initiatives_and_projects_pages-count': 0,
            'sidebar_menu_our_work_pages-count': 0,
            'sidebar_menu_about_us_pages-count': 0,
            }
        )

    # Test adding lead and feature stories to program and subprogram pages
    def test_adding_lead_story_to_program(self):
        self.program_page.lead_1 = self.article
        self.program_page.save()
        self.assertEqual(self.program_page.lead_1, self.article)

    def test_adding_lead_story_to_subprogram(self):
        self.subprogram_page.lead_1 = self.article
        self.subprogram_page.save()
        self.assertEqual(self.subprogram_page.lead_1, self.article)

    def test_adding_feature_story_to_program(self):
        self.program_page.feature_1 = self.article
        self.program_page.save()
        self.assertEqual(self.program_page.feature_1, self.article)

    def test_adding_feature_story_to_subprogram(self):
        self.subprogram_page.feature_1 = self.article
        self.subprogram_page.save()
        self.assertEqual(self.subprogram_page.feature_1, self.article)

    def test_adding_story_to_program_feature_carousel(self):
        self.program_page.feature_carousel.stream_data.append(
            {
                'type': 'event',
                'value': self.article.id
            }
        )
        self.assertEqual(
            self.program_page.feature_carousel.stream_data[0]['value'], 
            self.article.id
        )

    def test_adding_story_to_subprogram_feature_carousel(self):
        self.subprogram_page.feature_carousel.stream_data.append(
            {
                'type': 'event',
                'value': self.article.id
            }
        )
        self.assertEqual(
            self.subprogram_page.feature_carousel.stream_data[0]['value'], 
            self.article.id
        )

    # Test adding pages to the Program sidebar menu 
    def test_adding_about_us_pages_to_program_sidebar_menu(self):
        self.program_page.sidebar_menu_about_us_pages.stream_data.append(
            {
                'type': 'Item',
                'value': self.article.id
            }
        )
        self.assertEqual(
            self.program_page.sidebar_menu_about_us_pages.stream_data[0]['value'], 
            self.article.id
        )

    def test_adding_initiatives_and_projects_pages_to_program_sidebar_menu(self):
        self.program_page.sidebar_menu_initiatives_and_projects_pages.stream_data.append(
            {
                'type': 'Item',
                'value': self.article.id
            }
        )
        self.assertEqual(
            self.program_page.sidebar_menu_initiatives_and_projects_pages.stream_data[0]['value'], 
            self.article.id
        )

    def test_adding_our_work_pages_to_program_sidebar_menu(self):
        self.program_page.sidebar_menu_our_work_pages.stream_data.append(
            {
                'type': 'Item',
                'value': self.article.id
            }
        )
        self.assertEqual(
            self.program_page.sidebar_menu_our_work_pages.stream_data[0]['value'], 
            self.article.id
        )
