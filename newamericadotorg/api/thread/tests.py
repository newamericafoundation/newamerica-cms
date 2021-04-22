from rest_framework.test import APITestCase

from test_factories import PostFactory

from person.models import Person, PersonProgramRelationship, PersonSubprogramRelationship, PersonTopicRelationship
from thread.models import Thread, ThreadArticle, ThreadEdition

class ThreadAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        thread_home = home_page.add_child(instance=Thread(
            title='The Thread',
            slug='the-thread'
        ))

        cls.articles = PostFactory.create_content(8,
            content_page=thread_home,
            post_type=ThreadArticle
        )

    def test_article_list(self):
        url = '/api/thread/'
        result = self.client.get(url)
        data = result.json()

        self.assertEqual(len(data['results']), 8)

    def test_article_detail(self):
        url = '/api/thread/%s/' % self.articles[0].id
        result = self.client.get(url)
        data = result.json()

        self.assertEqual(data['id'], self.articles[0].id)
