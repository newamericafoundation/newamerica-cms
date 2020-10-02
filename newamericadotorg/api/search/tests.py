import datetime
import unittest
import random
from io import StringIO

from django.conf import settings
from django.core import management
from rest_framework.test import APITestCase, APIClient
from wagtail.core.models import PageViewRestriction
from wagtail.search.backends import get_search_backend

from test_factories import PostFactory

from blog.models import ProgramBlogPostsPage, BlogPost


TEST_ELASTICSEARCH = getattr(settings, "TEST_ELASTICSEARCH", False)


@unittest.skipUnless(TEST_ELASTICSEARCH, "Elasticsearch tests not enabled")
class SearchAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        program = PostFactory.create_program(home_page=home_page)

        cls.posts = PostFactory.create_program_content(50,
            program=program,
            content_page_type=ProgramBlogPostsPage,
            post_type=BlogPost,
            post_data={'title': 'Unique Query'}
        )

        # Some posts that shouldn't be returned in results
        PostFactory.create_program_content(10,
            program=program,
            content_page_type=ProgramBlogPostsPage,
            post_type=BlogPost,
            post_data={'title': 'Foo'}
        )

    def setUp(self):
        management.call_command('update_index', stdout=StringIO(), chunk_size=50)

    def test_search_all(self):
        url = '/api/search/?query=unique%20query'
        result = self.client.get(url).json()

        self.assertNotIn('error', result)
        self.assertEquals(result['count'], 50)

    def test_partial_match_disabled(self):
        url = '/api/search/?query=uniq'
        result = self.client.get(url).json()

        self.assertNotIn('error', result)
        self.assertEquals(result['count'], 0)

    def test_date_factored_into_ranking(self):
        # Seed the random number generators so the generated numbers are deterministic
        random.seed(a=123456, version=2)

        for post in self.posts:
            post.date = datetime.date.today() - datetime.timedelta(days=random.randint(0, 200) * 50)
            post.save()

        url = '/api/search/?query=unique query'
        response = self.client.get(url).json()

        self.assertNotIn('error', response)
        self.assertEquals(response['count'], 50)

        # Check that posts are returned in descending date order
        # This is only factored into the regular ranking algorithm, but in
        # this case all posts have the same title so the only ranking factor is
        # the date
        parse_date = lambda date_str: datetime.date(*map(int, date_str.split('-')))

        previous_date = parse_date(response['results'][0]['date'])
        for result in response['results'][1:]:
            date = parse_date(result['date'])
            self.assertTrue(date <= previous_date)

    def test_restricted(self):
        for p in self.posts[:25]:
            last_restriction = PageViewRestriction.objects.create(page=p, restriction_type=PageViewRestriction.PASSWORD)

        url = '/api/search/?query=unique%20query'
        result = self.client.get(url).json()

        self.assertNotIn('error', result)
        self.assertEquals(result['count'], 25)

        # Now check that the page appears in results when the restriction is passed
        session = self.client.session
        session[PageViewRestriction.passed_view_restrictions_session_key] = [last_restriction.id]
        session.save()

        url = '/api/search/?query=unique%20query'
        result = self.client.get(url).json()

        self.assertNotIn('error', result)
        self.assertEquals(result['count'], 26)
