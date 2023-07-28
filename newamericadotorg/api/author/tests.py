from django.urls import reverse
from rest_framework.test import APITestCase

from test_factories import PostFactory

from person.models import (
    PersonProgramRelationship,
    PersonSubprogramRelationship,
    PersonTopicRelationship,
)

from .serializers import AuthorSerializer


class AuthorAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        program = PostFactory.create_program(home_page=home_page)

        topics = PostFactory.create_program_topics(6, program=program)

        subtopic = PostFactory.create_subtopics(1, parent_topic=topics[0])[0]

        subprogram = PostFactory.create_subprogram(program=program)

        person = PostFactory.create_person()

        fellow = PostFactory.create_person(
            person_data={"role": "Fellow", "fellowship_year": 2016}
        )

        PostFactory.create_person(person_data={"former": True})

        PostFactory.create_person(person_data={"leadership": True})

        PostFactory.create_person(person_data={"role": "Board Member"})

        PersonProgramRelationship(program=program, person=person).save()

        PersonSubprogramRelationship(subprogram=subprogram, person=person).save()

        PersonTopicRelationship(topic=topics[0], person=person).save()

        PersonTopicRelationship(topic=subtopic, person=person).save()

        PersonProgramRelationship(program=program, person=fellow).save()

        PersonSubprogramRelationship(subprogram=subprogram, person=fellow).save()

        PersonTopicRelationship(topic=topics[0], person=fellow).save()

        cls.topics = topics
        cls.subtopic = subtopic

    def test_get_authors(self):
        url = "/api/author/"
        result = self.client.get(url)

        # excludes former and fellows
        self.assertEquals(result.json()["count"], 3)

    def test_get_include_fellows(self):
        url = "/api/author/?include_fellows=true"
        result = self.client.get(url)

        self.assertEquals(result.json()["count"], 4)

    def test_get_authors_by_topic(self):
        topic = self.topics[0]

        url = "/api/author/?include_fellows=true&topic_id=%s" % topic.id
        result = self.client.get(url)

        self.assertEquals(result.json()["count"], 2)

    def test_get_authors_by_subtopic(self):
        topic = self.subtopic

        url = "/api/author/?topic_id=%s" % topic.id
        result = self.client.get(url)

        self.assertEquals(result.json()["count"], 1)

    def test_get_authors_by_nonexistent_topic(self):
        url = "/api/author/?include_fellows=true&topic_id=5000"
        result = self.client.get(url)

        self.assertEquals(result.json()["count"], 0)

    def test_get_former(self):
        url = "/api/author/?former=true"
        result = self.client.get(url)

        self.assertEquals(result.json()["count"], 1)

    def test_get_leaders(self):
        url = "/api/author/?leadership=true"
        result = self.client.get(url)

        self.assertEquals(result.json()["count"], 1)

    def test_get_fellows(self):
        url = "/api/fellow/"
        result = self.client.get(url)

        self.assertEquals(result.json()["count"], 1)


class SortedAuthorAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        program1 = PostFactory.create_program(home_page=home_page)
        program2 = PostFactory.create_program(home_page=home_page)
        subprogram1 = PostFactory.create_subprogram(program=program1)

        person1 = PostFactory.create_person(
            {
                "sort_order": 2,
                "last_name": "Badger",
            }
        )
        person2 = PostFactory.create_person(
            {
                "sort_order": 3,
                "last_name": "Clam",
            }
        )
        person3 = PostFactory.create_person(
            {
                "sort_order": 1,
                "last_name": "Antelope",
            }
        )
        person4 = PostFactory.create_person(
            {
                "sort_order": 0,
                "last_name": "Aardvark",
            }
        )
        person5 = PostFactory.create_person(
            {
                "sort_order": None,
                "last_name": "Bear",
            }
        )

        PersonProgramRelationship(
            program=program1,
            person=person2,
            sort_order=2,
        ).save()
        PersonProgramRelationship(
            program=program1,
            person=person3,
            sort_order=3,
        ).save()
        PersonProgramRelationship(
            program=program1,
            person=person1,
            sort_order=1,
        ).save()
        PersonProgramRelationship(
            program=program1,
            person=person4,
            sort_order=1,
        ).save()
        PersonProgramRelationship(
            program=program1,
            person=person5,
            sort_order=None,
        ).save()

        PersonSubprogramRelationship(
            subprogram=subprogram1,
            person=person2,
            sort_order=2,
        ).save()
        PersonSubprogramRelationship(
            subprogram=subprogram1,
            person=person3,
            sort_order=3,
        ).save()
        PersonSubprogramRelationship(
            subprogram=subprogram1,
            person=person1,
            sort_order=1,
        ).save()
        PersonSubprogramRelationship(
            subprogram=subprogram1,
            person=person4,
            sort_order=1,
        ).save()
        PersonSubprogramRelationship(
            subprogram=subprogram1,
            person=person5,
            sort_order=None,
        ).save()

        cls.person1 = person1
        cls.person2 = person2
        cls.person3 = person3
        cls.person4 = person4
        cls.person5 = person5
        cls.program1 = program1
        cls.subprogram1 = subprogram1

    def test_global_order(self):
        response = self.client.get(reverse("author_list"))
        results = response.json()["results"]

        self.assertEqual(
            [self.person4.pk, self.person3.pk, self.person1.pk, self.person2.pk, self.person5.pk],
            [item["id"] for item in results],
        )

    def test_program_order(self):
        response = self.client.get(
            reverse("author_list"),
            {
                "program_id": self.program1.pk,
            },
        )
        results = response.json()["results"]

        expected = (
            PersonProgramRelationship.objects.filter(program=self.program1)
            .order_by("sort_order", "person__last_name")
            .select_related("person")
        )
        expected_serialized = [
            (
                AuthorSerializer(relationship.person).data["id"],
                AuthorSerializer(relationship.person).data["last_name"],
            )
            for relationship in expected
        ]

        self.assertEqual(
            expected_serialized,
            [(item["id"], item["last_name"]) for item in results],
        )

    def test_subprogram_order(self):
        response = self.client.get(
            reverse("author_list"),
            {
                "subprogram_id": self.subprogram1.pk,
            },
        )
        results = response.json()["results"]

        expected = (
            PersonSubprogramRelationship.objects.filter(
                subprogram=self.subprogram1,
            )
            .order_by("sort_order", "person__last_name")
            .select_related("person")
        )
        expected_serialized = [
            (
                AuthorSerializer(relationship.person).data["id"],
                AuthorSerializer(relationship.person).data["last_name"],
            )
            for relationship in expected
        ]

        self.assertEqual(
            expected_serialized,
            [(item["id"], item["last_name"]) for item in results],
        )
