from rest_framework.test import APITestCase

from wagtail.core.models import PageViewRestriction

from test_factories import PostFactory

from blog.models import ProgramBlogPostsPage, BlogPost

class SearchAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        program = PostFactory.create_program(home_page=home_page)

        posts = PostFactory.create_program_content(50,
            program=program,
            content_page_type=ProgramBlogPostsPage,
            post_type=BlogPost,
            post_data={'title': 'Unique Query'}
        )

        cls.posts = posts

    def test_search_all(self):
        url = '/api/search/?query=unique%20query'
        result = self.client.get(url).json()

        self.assertEquals(getattr(result, 'error', False), False)
        self.assertEquals(result['count'], 50)

    def test_restricted(self):
        for p in self.posts[:25]:
            PageViewRestriction(page=p).save()

        url = '/api/search/?query=unique%20query'
        result = self.client.get(url).json()

        self.assertEquals(getattr(result, 'error', False), False)
        self.assertEquals(result['count'], 25)
