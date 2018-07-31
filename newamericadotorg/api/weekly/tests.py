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

        editions = []
        for i in range(10):
            edition = weekly_home.add_child(instance=WeeklyEdition(
                title='Edition %s' % i,
                slug='edition-%s' % i
            ))

            editions.append(edition)

        articles = []
        for e in editions:
            articles_ = PostFactory.create_content(8,
                content_page=e,
                post_type=WeeklyArticle
            )

            articles = articles + articles_

        cls.editions = editions

    def test_edition_list(self):
        url = '/api/weekly/'
        result = self.client.get(url)
        data = result.json()

        self.assertEquals(data['count'], 10)

    def test_edition_detail(self):
        url = '/api/weekly/%s/' % self.editions[0].id
        result = self.client.get(url)
        data = result.json()

        self.assertEquals(len(data['articles']), 8)
        self.assertEquals(data['title'], data['articles'][0]['title'])
