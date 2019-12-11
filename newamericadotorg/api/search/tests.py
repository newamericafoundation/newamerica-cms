from io import StringIO

from django.core import management
from rest_framework.test import APITestCase, APIClient
from wagtail.core.models import PageViewRestriction
from wagtail.search.backends import get_search_backend

from test_factories import PostFactory

from blog.models import ProgramBlogPostsPage, BlogPost

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
