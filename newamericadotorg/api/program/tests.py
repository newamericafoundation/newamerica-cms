from rest_framework.test import APITestCase

from test_factories import PostFactory

from programs.models import Program, Subprogram, FeaturedProgramPage, FeaturedSubprogramPage, SubscriptionProgramRelationship, SubscriptionSubprogramRelationship
from issue.models import IssueOrTopic
from home.models import ProgramAboutHomePage, ProgramAboutPage
from blog.models import ProgramBlogPostsPage, BlogPost
from subscribe.models import SubscriptionSegment, SubscribePage
from issue.models import TopicHomePage, IssueOrTopic

class ProgramAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()
        subpage = home_page.add_child(instance=SubscribePage(
            title='Subscriptions'
        ))
        segment = subpage.add_child(instance=SubscriptionSegment(
            title='Sub Segment',
            SegmentID='0',
            ListID='0'
        ))

        program = PostFactory.create_program(home_page=home_page)
        cls.program = program
        program_about_home = program.add_child(instance=ProgramAboutHomePage(
            title='About',
            slug='about'
        ))

        cls.program_posts = PostFactory.create_program_content(5,
            program=program,
            content_page_type=ProgramBlogPostsPage,
            post_type=BlogPost
        )

        FeaturedProgramPage(
            program=program,
            page=cls.program_posts[0]
        ).save()

        SubscriptionProgramRelationship(
            subscription_segment=segment,
            program=program
        ).save()

        program_about = program_about_home.add_child(instance=ProgramAboutPage(
            title='About Subpage',
            slug='subpage',
            show_in_menus=True
        ))

        subprogram = PostFactory.create_subprogram(program=program)
        cls.subprogram = subprogram

        FeaturedSubprogramPage(
            program=subprogram,
            page=cls.program_posts[1]
        ).save()

        SubscriptionSubprogramRelationship(
            subscription_segment=segment,
            subprogram=subprogram
        ).save()

        subprogram_about_home = subprogram.add_child(instance=ProgramAboutHomePage(
            title='About',
            slug='about'
        ))

        subprogram_about = subprogram_about_home.add_child(instance=ProgramAboutPage(
            title='About Subpage',
            slug='subpage',
            show_in_menus=True
        ))


    def test_program_list(self):
        url = '/api/program/'
        response = self.client.get(url)

        self.assertEqual(response.json()['count'], 1)

    def test_subprogram_list(self):
        url = '/api/subprogram/'
        response = self.client.get(url)

        self.assertEqual(response.json()['count'], 1)

    def test_get_program(self):
        url = '/api/program/%s/' % self.program.id
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(data['title'], self.program.title)
        self.assertEqual(data['about']['subpages'][0]['slug'], 'subpage')
        self.assertEqual(data['subprograms'][0]['title'], self.subprogram.title)
        self.assertEqual(data['story_grid']['pages'][0]['title'], self.program_posts[0].title)
        self.assertEqual(data['content_types'][0]['api_name'], 'blogpost')
        self.assertEqual(data['subscriptions'][0]['title'], 'Sub Segment')
        # only retrieves subpages that are not Content pages
        # so should only return Subprogram and About Home Page here
        self.assertEqual(len(data['subpages']), 2)
        self.assertEqual(data['topics'], False)

    def test_program_topic(self):
        program_topic_home = self.program.add_child(instance=TopicHomePage(
            title='Topic'
        ))

        program_topic_home.add_child(instance=IssueOrTopic(
            title='Topic Child'
        ))

        url = '/api/program/%s/' % self.program.id
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(data['topics'], True)

    def test_get_subprogram(self):
        url = '/api/subprogram/%s/' % self.subprogram.id
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(data['title'], self.subprogram.title)
        self.assertEqual(data['about']['subpages'][0]['slug'], 'subpage')
        self.assertEqual(data['story_grid']['pages'][0]['title'], self.program_posts[1].title)
        self.assertEqual(data['subscriptions'][0]['title'], 'Sub Segment')
        # only retrieves subpages that are not Content pages
        # so should only return About Home Page
        self.assertEqual(len(data['subpages']), 1)
