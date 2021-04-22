from rest_framework.test import APITestCase

from test_factories import PostFactory

from person.models import Person, PersonProgramRelationship, PersonSubprogramRelationship, PersonTopicRelationship
from weekly.models import Weekly, WeeklyArticle, WeeklyEdition

class WeeklyAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        weekly_home = home_page.add_child(instance=Weekly(
            title='Weekly',
            slug='weekly'
        ))

        cls.articles = PostFactory.create_content(8,
            content_page=weekly_home,
            post_type=WeeklyArticle
        )

    def test_article_list(self):
        url = '/api/weekly/'
        result = self.client.get(url)
        data = result.json()

        self.assertEqual(len(data['results']), 8)

    def test_article_detail(self):
        url = '/api/weekly/%s/' % self.articles[0].id
        result = self.client.get(url)
        data = result.json()

        self.assertEqual(data['id'], self.articles[0].id)
