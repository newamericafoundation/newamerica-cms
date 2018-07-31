from datetime import date, timedelta
from rest_framework.test import APITestCase

from test_factories import PostFactory

from event.models import Event, ProgramEventsPage
from programs.models import Program, Subprogram
from blog.models import ProgramBlogPostsPage, BlogPost

class PostAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        program = PostFactory.create_program(home_page=home_page)

        PostFactory.create_program_content(15,
            program=program,
            content_page_type=ProgramEventsPage,
            post_type=Event,
            content_page_data={
                'title': 'Events',
                'slug': 'events'
            },
            post_data={
                'date': date(2015,11,1)
            }
        )

        event_home = ProgramEventsPage.objects.first()

        PostFactory.create_content(5,
            content_page=event_home,
            post_type=Event,
            post_data={
                'date': date.today() + timedelta(days=1)
            }
        )

        PostFactory.create_content(5,
            content_page=event_home,
            post_type=Event,
            post_data={
                'date': date.today()
            }
        )

    def test_get_future(self):
        url = '/api/event/?time_period=future'
        result = self.client.get(url)

        self.assertEqual(result.json()['count'], 10)

    def test_get_past(self):
        url = '/api/event/?time_period=past'
        result = self.client.get(url)

        self.assertEqual(result.json()['count'], 15)

    def test_query_after_date(self):
        d = date.today() + timedelta(days=1)
        d = d.strftime('%Y-%m-%d')
        url = '/api/event/?after=%s' % d
        result = self.client.get(url)

        self.assertEqual(result.json()['count'], 5)

    def test_query_before_date(self):
        d = date.today() - timedelta(days=1)
        d = d.strftime('%Y-%m-%d')
        url = '/api/event/?before=%s' % d
        result = self.client.get(url)

        self.assertEqual(result.json()['count'], 15)
