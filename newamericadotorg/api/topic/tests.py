from rest_framework.test import APITestCase

from test_factories import PostFactory

from person.models import Person, PersonProgramRelationship, PersonSubprogramRelationship, PersonTopicRelationship
from issue.models import IssueOrTopic

class TopicAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        program = PostFactory.create_program(home_page=home_page)

        program2 = PostFactory.create_program(home_page=home_page)

        topics = PostFactory.create_program_topics(6,
            program=program
        )

        topics2 = PostFactory.create_program_topics(6,
            program=program2
        )

        subtopics = PostFactory.create_subtopics(8,
            parent_topic=topics[0]
        )

        sub_subtopics = PostFactory.create_subtopics(3,
            parent_topic=subtopics[0]
        )

        cls.program = program
        cls.topics = topics

    def test_topic_list(self):
        url = '/api/topic/'
        result = self.client.get(url)

        self.assertEquals(result.json()['count'], 12)

    def test_topic_detail(self):
        url = '/api/topic/%s/' % self.topics[0].id
        result = self.client.get(url)
        data = result.json()

        self.assertEquals(len(data['subtopics']), 8)
        self.assertEquals(data['program']['title'], self.program.title)

    def test_topic_list_by_program(self):
        url = '/api/topic/?program_id=%s' % self.program.id
        result = self.client.get(url)
        data = result.json()

        self.assertEquals(data['count'], 6)
