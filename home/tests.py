import datetime
from datetime import date, timedelta

from django.http import HttpResponsePermanentRedirect
from django.test import Client, TestCase
from wagtail import blocks
from wagtail.images import get_image_model
from wagtail.images.tests.utils import get_test_image_file
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase
from wagtail.test.utils.form_data import nested_form_data

from article.models import AllArticlesHomePage, Article, ProgramArticlesPage
from blog.models import AllBlogPostsHomePage
from book.models import AllBooksHomePage
from brief.models import AllBriefsHomePage
from collection.models import CollectionsHomePage
from conference.models import AllConferencesHomePage
from future_security_forum.models import FutureSecurityForumPage
from event.models import AllEventsHomePage, Event, ProgramEventsPage
from in_depth.models import AllInDepthHomePage
from other_content.models import AllOtherPostsHomePage, FullPageEmbed
from person.models import BoardAndLeadershipPeoplePage, OurPeoplePage
from podcast.models import AllPodcastsHomePage
from policy_paper.models import (
    AllPolicyPapersHomePage,
)
from press_release.models import AllPressReleasesHomePage
from programs.models import Program, PublicationsPage, Subprogram
from quoted.models import AllQuotedHomePage
from report.models import AllReportsHomePage
from test_factories import PostFactory
from the_thread.models import AllThreadArticlesHomePage, Thread
from weekly.models import AllWeeklyArticlesHomePage, Weekly

from .blocks import ExternalLeadStoryBlock
from .models import (
    HomePage,
    JobsPage,
    OrgSimplePage,
    ProjectRequests,
    ProgramAboutHomePage,
    ProgramSimplePage,
    RedirectPage,
    SubscribePage,
)

WagtailImage = get_image_model()


class HomeTests(WagtailPageTestCase):
    """
    Testing hierarchies between pages and whether it is possible
    to create a Homepage and all the allowed subpages
    underneath the Homepage.

    Testing functionality of OrgSimplePage and ProgramSimplePage.
    """

    def setUp(self):
        self.login()
        site = Site.objects.get()
        page = Page.get_first_root_node()
        home = HomePage(title='New America')
        self.home_page = page.add_child(instance=home)
        self.root_page = Page.objects.get(id=1)

        site.root_page = home
        site.save()

        self.home_page.add_child(
            instance=AllEventsHomePage(title="Events")
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
        self.program_articles_page = self.program_page.add_child(
            instance=ProgramArticlesPage(title='Program Articles')
        )
        self.article = self.program_articles_page.add_child(
            instance=Article(
                title='Article 1',
                date='2016-02-02'
            )
        )
        self.article.save()

        self.program_events_page = self.program_page.add_child(
            instance=ProgramEventsPage(title='OTI Events', slug='oti-events')
        )
        self.today_event = self.program_events_page.add_child(
            instance=Event(
                title='Today Event' ,
                date=str(date.today()),
                rsvp_link='http://www.newamerica.org',
                soundcloud_url='http://www.newamerica.org'
            )
        )
        self.future_event_morning = self.program_events_page.add_child(
            instance=Event(
                title='Future Event' ,
                date=str(date.today()+timedelta(days=5)),
                start_time=str((datetime.datetime.now()-timedelta(hours=5)).time()),
                rsvp_link='http://www.newamerica.org',
                soundcloud_url='http://www.newamerica.org'
            )
        )
        self.future_event_afternoon = self.program_events_page.add_child(
            instance=Event(
                title='Future Event' ,
                date=str(date.today()+timedelta(days=5)),
                start_time=str((datetime.datetime.now()+timedelta(hours=5)).time()),
                rsvp_link='http://www.newamerica.org',
                soundcloud_url='http://www.newamerica.org'
            )
        )
        self.past_event = self.program_events_page.add_child(
            instance=Event(
                title='Past Event',
                date=str(date.today()-timedelta(days=5)),
                rsvp_link='http://www.newamerica.org',
                soundcloud_url='http://www.newamerica.org'
            )
        )
        self.today_early_morning_event = self.program_events_page.add_child(
            instance=Event(
                title='Early Morning Event',
                date=str(date.today()),
                start_time=str((datetime.datetime.now()-timedelta(hours=5)).time()),
                rsvp_link='http://www.newamerica.org',
                soundcloud_url='http://www.newamerica.org'
            )
        )
        self.multiday_event_ending_today = self.program_events_page.add_child(
            instance=Event(
                title='Early Morning Event',
                date=str(date.today()-timedelta(days=5)),
                end_date=str(date.today()),
                rsvp_link='http://www.newamerica.org',
                soundcloud_url='http://www.newamerica.org'
            )
        )


    def test_can_create_homepage_under_root_page(self):
        parent_page = Page.get_first_root_node()
        home = HomePage(title='New America')
        parent_page.add_child(instance=home)

    # Test that a particular child Page type
    # can be created under a parent Page type
    def test_homepage_parent_page_type(self):
        self.assertCanCreateAt(Page, HomePage)

    # Test that the only page types that can be created
    # under parent_model are child_models
    def test_homepage_subpages(self):
        self.assertAllowedSubpageTypes(HomePage, {
            AllArticlesHomePage,
            AllBooksHomePage,
            AllBlogPostsHomePage,
            AllEventsHomePage,
            AllPodcastsHomePage,
            AllPolicyPapersHomePage,
            AllPressReleasesHomePage,
            AllQuotedHomePage,
            AllInDepthHomePage,
            AllConferencesHomePage,
            BoardAndLeadershipPeoplePage,
            JobsPage,
            OurPeoplePage,
            OrgSimplePage,
            ProjectRequests,
            Program,
            SubscribePage,
            Weekly,
            Thread,
            RedirectPage,
            AllReportsHomePage,
            PublicationsPage,
            AllBriefsHomePage,
            AllOtherPostsHomePage,
            FullPageEmbed,
            AllThreadArticlesHomePage,
            AllWeeklyArticlesHomePage,
            CollectionsHomePage,
            FutureSecurityForumPage,
            })

    # Test that pages can be created with POST data
    def test_can_create_homepage_under_page(self):
        self.assertCanCreate(self.root_page, HomePage, nested_form_data({
            'title': 'New America 2',
            'slug': 'new-america-2',
            'subscriptions': {
                'TOTAL_FORMS': 0,
                'INITIAL_FORMS': 0,
                'MIN_NUM_FORMS': 0,
                'MAX_NUM_FORMS': 1000
            },
            'recent_carousel': {
                'count': 0
            },
            'about_pages': {
                'count': 0
            },
            'lead_stories': {
                'count': 0
            },
          })
        )

    def test_can_create_program_under_homepage_with_data(self):
        self.assertCanCreate(self.home_page, Program, nested_form_data({
            'title': 'OTI2',
            'name': 'OTI2',
            'description': 'OTI2',
            'slug': 'oti-2',
            'depth': 3,
            'featured_pages': {
                'TOTAL_FORMS': 0,
                'INITIAL_FORMS': 0,
                'MIN_NUM_FORMS': 0,
                'MAX_NUM_FORMS': 1000
            },
            'subscriptions': {
                'TOTAL_FORMS': 0,
                'INITIAL_FORMS': 0,
                'MIN_NUM_FORMS': 0,
                'MAX_NUM_FORMS': 1000
            },
            'feature_carousel': {
                'count': 0
            },
            'sidebar_menu_initiatives_and_projects_pages' : {
                'count': 0
            },
            'sidebar_menu_our_work_pages': {
                'count': 0
            },
            'sidebar_menu_about_us_pages': {
                'count': 0
            }
          })
        )

    def test_adding_lead_stories_to_homepage(self):
        # Create mock Wagtail image.
        test_image_file = get_test_image_file(filename="test.jpg")
        mock_image = WagtailImage.objects.create(
            title="test.jpg",
            file=test_image_file,
        )

        # Create example external link.
        external_link = {
            "link": "https://www.example.com/",
            "image": mock_image.pk,
            "image_alt": "Some alt text",
            "heading": "Some heading",
            "description": "Some description. Lorem ipsum.",
            "tag": "External Link",
        }

        # Populate lead stories.
        self.home_page.lead_stories = [
            ("internal", blocks.PageChooserBlock().to_python(self.article.pk)),
            ("external", ExternalLeadStoryBlock().to_python(external_link)),
        ]
        self.home_page.save()

        # Check if the homepage has the correct data.
        self.home_page.refresh_from_db()
        self.assertEqual(self.home_page.lead_stories[0].value.specific, self.article)
        self.assertEqual(
            ExternalLeadStoryBlock().get_prep_value(self.home_page.lead_stories[1].value),
            external_link,
        )

    def test_adding_feature_story_to_homepage(self):
        self.home_page.feature_1 = self.article
        self.home_page.save()
        self.assertEqual(self.home_page.feature_1, self.article)

    def test_adding_org_simple_page(self):
        simple_page = OrgSimplePage(
            title='Org Simple Page Test'
        )
        self.home_page.add_child(instance=simple_page)
        self.assertEqual(simple_page.content_type,
            self.home_page.get_children().filter(
            title='Org Simple Page Test')[0].content_type
        )

    def test_adding_excerpt_to_simple_page(self):
        excerpt = 'This is a cool excerpt!'
        simple_page = OrgSimplePage(
            title='Org Simple Page Test',
            story_excerpt=excerpt
        )
        self.home_page.add_child(instance=simple_page)
        self.assertEqual(excerpt, OrgSimplePage.objects.first().story_excerpt)


    def test_adding_program_simple_page(self):
        program_simple_page = ProgramSimplePage(
            title='Program Simple Page Test'
        )
        self.program_page.add_child(instance=program_simple_page)
        self.assertEqual(program_simple_page.content_type,
            self.program_page.get_children().filter(
            title='Program Simple Page Test')[0].content_type
        )

    def test_redirect_page_under_home_page(self):
        redirect_page = RedirectPage(
            title='Google',
            redirect_url = 'https://www.google.com',
        )
        self.home_page.add_child(instance=redirect_page)
        c = Client()
        response = c.get('http://localhost:8000/google')
        self.assertTrue(isinstance(response, HttpResponsePermanentRedirect))

    def test_adding_redirect_page_under_program_page(self):
        redirect_page = RedirectPage(
            title='Google',
            redirect_url = 'https://www.google.com',
        )
        self.program_page.add_child(instance=redirect_page)
        c = Client()
        response = c.get('http://localhost:8000/oti/google')
        self.assertTrue(isinstance(response, HttpResponsePermanentRedirect))

    def test_adding_redirect_page_under_subprogram_page(self):
        subprogram = Subprogram(
            title='Test',
            name='Test',
            description='Test',
        )
        self.program_page.add_child(instance=subprogram)
        redirect_page = RedirectPage(
            title='Google',
            redirect_url = 'https://www.google.com',
        )
        subprogram.add_child(instance=redirect_page)
        c = Client()
        response = c.get('http://localhost:8000/oti/test/google')
        self.assertTrue(isinstance(response, HttpResponsePermanentRedirect))

    def test_adding_redirect_page_under_simple_page(self):
        simple_page = OrgSimplePage(
            title='Simple'
        )
        self.home_page.add_child(instance=simple_page)
        redirect_page = RedirectPage(
            title='Google',
            redirect_url = 'https://www.google.com',
        )
        simple_page.add_child(instance=redirect_page)
        c = Client()
        response = c.get('http://localhost:8000/simple/google')
        self.assertTrue(isinstance(response, HttpResponsePermanentRedirect))

    def test_article_has_correct_ordered_date_string(self):
        self.assertEqual(
            self.article.ordered_date_string, f'{str(self.article.date)}-{self.article.id}'
        )


class TestProgramAboutHomePage(TestCase):
    @classmethod
    def setUpTestData(cls):
        # cls.login()
        # site = Site.objects.get()
        # page = Page.get_first_root_node()
        # home = HomePage(title='New America')
        # cls.home_page = page.add_child(instance=home)
        # cls.root_page = Page.objects.get(id=1)

        # site.root_page = home
        # site.save()
        home_page = PostFactory.create_homepage()
        cls.program = PostFactory.create_program(home_page=home_page)

    def test_program_about_homepage_sets_slug_to_about(self):
        page = ProgramAboutHomePage(
            title='Page title',
            slug='not-about',
        )
        added_page = self.program.add_child(instance=page)
        self.assertEqual(Page.objects.get(pk=added_page.pk).slug, 'about')
