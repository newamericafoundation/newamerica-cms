from rest_framework.test import APITestCase

from test_factories import PostFactory

from person.models import Person, PersonProgramRelationship, PersonSubprogramRelationship, PersonTopicRelationship
from issue.models import IssueOrTopic

class AuthorAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        program = PostFactory.create_program(home_page=home_page)

        topics = PostFactory.create_program_topics(6,
            program=program
        )

        subtopic = PostFactory.create_subtopics(1,
            parent_topic=topics[0]
        )[0]

        subprogram = PostFactory.create_subprogram(program=program)

        person = PostFactory.create_person()

        fellow = PostFactory.create_person(
            person_data={
                'role': 'Fellow',
                'fellowship_year': 2016
            }
        )

        former_person = PostFactory.create_person(
            person_data={
                'former': True
            }
        )

        leader = PostFactory.create_person(
            person_data={
                'leadership': True
            }
        )

        board_member = PostFactory.create_person(
            person_data={
                'role': 'Board Member'
            }
        )

        PersonProgramRelationship(
            program=program,
            person=person
        ).save()

        PersonSubprogramRelationship(
            subprogram=subprogram,
            person=person
        ).save()

        PersonTopicRelationship(
            topic=topics[0],
            person=person
        ).save()

        PersonTopicRelationship(
            topic=subtopic,
            person=person
        ).save()

        PersonProgramRelationship(
            program=program,
            person=fellow
        ).save()

        PersonSubprogramRelationship(
            subprogram=subprogram,
            person=fellow
        ).save()

        PersonTopicRelationship(
            topic=topics[0],
            person=fellow
        ).save()

        cls.topics = topics
        cls.subtopic = subtopic

    def test_get_authors(self):
        url = '/api/author/'
        result = self.client.get(url)

        # excludes former and fellows
        self.assertEquals(result.json()['count'], 3)

    def test_get_include_fellows(self):
        url = '/api/author/?include_fellows=true'
        result = self.client.get(url)

        self.assertEquals(result.json()['count'], 4)

    def test_get_authors_by_topic(self):
        topic = self.topics[0]

        url = '/api/author/?include_fellows=true&topic_id=%s' % topic.id
        result = self.client.get(url)

        self.assertEquals(result.json()['count'], 2)

    def test_get_authors_by_subtopic(self):
        topic = self.subtopic

        url = '/api/author/?topic_id=%s' % topic.id
        result = self.client.get(url)

        self.assertEquals(result.json()['count'], 1)

    def test_get_authors_by_nonexistent_topic(self):
        url = '/api/author/?include_fellows=true&topic_id=5000'
        result = self.client.get(url)

        self.assertEquals(result.json()['count'], 0)

    def test_get_former(self):
        url = '/api/author/?former=true'
        result = self.client.get(url)

        self.assertEquals(result.json()['count'], 1)

    def test_get_leaders(self):
        url = '/api/author/?leadership=true'
        result = self.client.get(url)

        self.assertEquals(result.json()['count'], 1)

    def test_get_fellows(self):
        url = '/api/fellow/'
        result = self.client.get(url)

        self.assertEquals(result.json()['count'], 1)

    def test_get_fellows_by_year(self):
        url = '/api/fellow/?fellowship_year=2010'
        result = self.client.get(url)

        self.assertEquals(result.json()['count'], 0)
