# vagrant ssh -c 'ELASTICSEARCH_URL=http://localhost:9200 SECRET_KEY=test DJANGO_SETTINGS_MODULE=newamericadotorg.settings.dev PGDATABASE=newamerica-cms DATABASE_URL=postgres:///newamerica-cms PYTHONPATH=/vagrant /home/vagrant/.virtualenvs/newamerica-cms/bin/django-admin.py test --noinput --failfast --keepdb newamericadotorg.api.search.tests'
from pprint import pprint
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
from event.models import Event, ProgramEventsPage
from person.models import (
    PersonProgramRelationship,
    PersonSubprogramRelationship,
    Person,
)
from issue.models import TopicHomePage, IssueOrTopic


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


@unittest.skipUnless(TEST_ELASTICSEARCH, "Elasticsearch tests not enabled")
class SearchPeopleAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        program = PostFactory.create_program(home_page=home_page)

        cls.person1 = PostFactory.create_person(person_data={
            'title': 'Alice',
        })

        cls.person2 = PostFactory.create_person(person_data={
            'title': 'Bob',
        })

        # Some posts that shouldn't be returned in results
        PostFactory.create_program_content(10,
            program=program,
            content_page_type=ProgramBlogPostsPage,
            post_type=BlogPost,
            post_data={'title': 'Alice'}
        )
        cls.home_page = home_page

    def setUp(self):
        management.call_command('update_index', stdout=StringIO(), chunk_size=50)

    def test_search_person(self):
        url = '/api/search/people/?query=alice'
        result = self.client.get(url).json()

        self.assertNotIn('error', result)
        self.assertEquals(result['count'], 1)
        self.assertEquals(result['results'][0]['id'], self.person1.pk)


@unittest.skipUnless(TEST_ELASTICSEARCH, "Elasticsearch tests not enabled")
class SearchProgramsAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        cls.program = PostFactory.create_program(
            home_page=home_page,
            program_data={
                'title': 'Robots Program'
            }
        )

        cls.program2 = PostFactory.create_program(
            home_page=home_page,
            program_data={
                'title': 'Birds Program'
            }
        )

        cls.subprogram = PostFactory.create_subprogram(
            program=cls.program,
            subprogram_data={
                'title': 'Robots Subprogram',
            },
        )

        # Some posts that shouldn't be returned in results
        PostFactory.create_program_content(10,
            program=cls.program,
            content_page_type=ProgramBlogPostsPage,
            post_type=BlogPost,
            post_data={'title': 'Robots'}
        )

    def setUp(self):
        management.call_command('update_index', stdout=StringIO(), chunk_size=50)

    def test_search_programs(self):
        url = '/api/search/programs/?query=robots'
        result = self.client.get(url).json()

        self.assertNotIn('error', result)
        self.assertEquals(result['count'], 2)

        ids = set(r['id'] for r in result['results'])

        self.assertIn(self.program.pk, ids)
        self.assertIn(self.subprogram.pk, ids)


@unittest.skipUnless(TEST_ELASTICSEARCH, "Elasticsearch tests not enabled")
class SearchUpcomingEventsAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        cls.program = PostFactory.create_program(
            home_page=home_page,
            program_data={
                'title': 'Robots Program'
            }
        )

        cls.future_party = PostFactory.create_program_content(
            1,
            program=cls.program,
            content_page_type=ProgramEventsPage,
            post_type=Event,
            content_page_data={},
            post_data={
                'title': 'Party',
                'date': datetime.date.today() + datetime.timedelta(days=1),
            }
        )

        PostFactory.create_program_content(
            1,
            program=cls.program,
            content_page_type=ProgramEventsPage,
            post_type=Event,
            content_page_data={},
            post_data={
                'title': 'Study hall',
                'date': datetime.date.today() + datetime.timedelta(days=1),
            }
        )

        PostFactory.create_program_content(
            1,
            program=cls.program,
            content_page_type=ProgramEventsPage,
            post_type=Event,
            content_page_data={},
            post_data={
                'title': 'Party',
                'date': datetime.date.today() - datetime.timedelta(days=1),
            }
        )

        # Some posts that shouldn't be returned in results
        PostFactory.create_program_content(10,
            program=cls.program,
            content_page_type=ProgramBlogPostsPage,
            post_type=BlogPost,
            post_data={'title': 'Party'}
        )

    def setUp(self):
        management.call_command('update_index', stdout=StringIO(), chunk_size=50)

    def test_search_upcoming(self):
        url = '/api/search/upcoming_events/?query=party'
        result = self.client.get(url).json()

        self.assertNotIn('error', result)
        self.assertEquals(result['count'], 1)
        self.assertEquals(result['results'][0]['id'], self.future_party[0].pk)


@unittest.skipUnless(TEST_ELASTICSEARCH, "Elasticsearch tests not enabled")
class SearchPastEventsAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        cls.program = PostFactory.create_program(
            home_page=home_page,
            program_data={
                'title': 'Party Program'
            }
        )

        cls.future_party = PostFactory.create_program_content(
            1,
            program=cls.program,
            content_page_type=ProgramEventsPage,
            post_type=Event,
            content_page_data={},
            post_data={
                'title': 'Party',
                'date': datetime.date.today() + datetime.timedelta(days=1),
            }
        )

        PostFactory.create_program_content(
            1,
            program=cls.program,
            content_page_type=ProgramEventsPage,
            post_type=Event,
            content_page_data={},
            post_data={
                'title': 'Study hall',
                'date': datetime.date.today() - datetime.timedelta(days=1),
            }
        )

        cls.past_party = PostFactory.create_program_content(
            1,
            program=cls.program,
            content_page_type=ProgramEventsPage,
            post_type=Event,
            content_page_data={},
            post_data={
                'title': 'Party',
                'date': datetime.date.today() - datetime.timedelta(days=1),
            }
        )

        cls.posts = PostFactory.create_program_content(2,
            program=cls.program,
            content_page_type=ProgramBlogPostsPage,
            post_type=BlogPost,
            post_data={'title': 'Party'}
        )

    def setUp(self):
        management.call_command('update_index', stdout=StringIO(), chunk_size=50)

    def test_search_past(self):
        url = '/api/search/pubs_and_past_events/?query=party'
        result = self.client.get(url).json()
        ids = set(r['id'] for r in result['results'])

        self.assertNotIn('error', result)
        self.assertEquals(result['count'], 3)
        self.assertIn(self.past_party[0].pk, ids)
        for post in self.posts:
            self.assertIn(post.pk, ids)


@unittest.skipUnless(TEST_ELASTICSEARCH, "Elasticsearch tests not enabled")
class SearchOtherPagesAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        cls.program = PostFactory.create_program(
            home_page=home_page,
            program_data={
                'title': 'Octopus Program'
            }
        )

        PostFactory.create_program_content(
            1,
            program=cls.program,
            content_page_type=ProgramEventsPage,
            post_type=Event,
            content_page_data={},
            post_data={
                'title': 'Octopus',
                'date': datetime.date.today() + datetime.timedelta(days=1),
            }
        )

        PostFactory.create_program_content(
            1,
            program=cls.program,
            content_page_type=ProgramEventsPage,
            post_type=Event,
            content_page_data={},
            post_data={
                'title': 'Study hall',
                'date': datetime.date.today() - datetime.timedelta(days=1),
            }
        )

        PostFactory.create_program_content(
            1,
            program=cls.program,
            content_page_type=ProgramEventsPage,
            post_type=Event,
            content_page_data={},
            post_data={
                'title': 'Study hall',
                'date': datetime.date.today() - datetime.timedelta(days=1),
            }
        )

        PostFactory.create_program_content(2,
            program=cls.program,
            content_page_type=ProgramBlogPostsPage,
            post_type=BlogPost,
            post_data={'title': 'Octopus'}
        )

        cls.topics = PostFactory.create_program_topics(
            3,
            program=cls.program,
            topic_data={'title': 'Octopus'}
        )

    def setUp(self):
        management.call_command('update_index', stdout=StringIO(), chunk_size=50)

    def test_search_other(self):
        url = '/api/search/other/?query=octopus'
        result = self.client.get(url).json()
        ids = set(r['id'] for r in result['results'])

        self.assertNotIn('error', result)
        self.assertEquals(result['count'], 3)


@unittest.skipUnless(TEST_ELASTICSEARCH, "Elasticsearch tests not enabled")
class SearchPeopleFilterByProgramTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        program = PostFactory.create_program(home_page=home_page)

        cls.person1 = PostFactory.create_person(person_data={
            'title': 'Alice',
        })

        cls.program2 = PostFactory.create_program(home_page=home_page)
        cls.person2 = PostFactory.create_person(person_data={
            'title': 'Alice 2',
        })

        PersonProgramRelationship.objects.create(
            program=cls.program2,
            person=cls.person2
        )

    def setUp(self):
        management.call_command('update_index', stdout=StringIO(), chunk_size=50)
        url = f'/api/search/people/?query=alice&program_id={self.program2.pk}'
        self.response = self.client.get(url)
        self.json = self.response.json()

    def test_returns_success_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_returns_exactly_one_person(self):
        self.assertEquals(self.json['count'], 1)
        self.assertEquals(len(self.json['results']), 1)

    def test_returns_correct_response_body(self):
        self.assertEqual(self.json['results'][0]['title'], self.person2.title)
        self.assertEqual(self.json['results'][0]['id'], self.person2.pk)


@unittest.skipUnless(TEST_ELASTICSEARCH, "Elasticsearch tests not enabled")
class SearchPeopleFilterBySubprogramTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        program = PostFactory.create_program(home_page=home_page)

        cls.subprogram1 = PostFactory.create_subprogram(
            program=program,
            subprogram_data={
                'title': 'Octopus Subprogram',
            },
        )
        cls.subprogram2 = PostFactory.create_subprogram(
            program=program,
            subprogram_data={
                'title': 'Squid Subprogram',
            },
        )

        cls.person1 = PostFactory.create_person(person_data={
            'title': 'Alice',
        })

        cls.person2 = PostFactory.create_person(person_data={
            'title': 'Alice 2',
        })

        PersonSubprogramRelationship.objects.create(
            subprogram=cls.subprogram2,
            person=cls.person2,
        )

        PersonSubprogramRelationship.objects.create(
            subprogram=cls.subprogram1,
            person=cls.person1,
        )

    def setUp(self):
        management.call_command('update_index', stdout=StringIO(), chunk_size=50)
        url = f'/api/search/people/?query=alice&subprogram_id={self.subprogram2.pk}'
        self.response = self.client.get(url)
        self.json = self.response.json()

    def test_returns_success_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_returns_exactly_one_person(self):
        self.assertEquals(self.json['count'], 1)
        self.assertEquals(len(self.json['results']), 1)

    def test_returns_correct_response_body(self):
        self.assertEqual(self.json['results'][0]['title'], self.person2.title)
        self.assertEqual(self.json['results'][0]['id'], self.person2.pk)


@unittest.skipUnless(TEST_ELASTICSEARCH, "Elasticsearch tests not enabled")
class SearchOtherPagesFilterByProgramTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        cls.program1 = PostFactory.create_program(home_page=home_page)
        cls.program2 = PostFactory.create_program(home_page=home_page)

        cls.topic1 = PostFactory.create_program_topics(
            1,
            program=cls.program1,
            topic_data={'title': 'Octopus'}
        )[0]
        cls.topic2 = PostFactory.create_program_topics(
            1,
            program=cls.program2,
            topic_data={'title': 'Octopus'}
        )[0]

    def setUp(self):
        management.call_command('update_index', stdout=StringIO(), chunk_size=50)
        url = f'/api/search/other/?query=octopus&program_id={self.program2.pk}'
        self.response = self.client.get(url)
        self.json = self.response.json()

    def test_returns_success_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_returns_exactly_one_post(self):
        self.assertEquals(self.json['count'], 1)
        self.assertEquals(len(self.json['results']), 1)

    def test_returns_correct_response_body(self):
        self.assertEqual(self.json['results'][0]['title'], self.topic2.title)
        self.assertEqual(self.json['results'][0]['id'], self.topic2.pk)


@unittest.skipUnless(TEST_ELASTICSEARCH, "Elasticsearch tests not enabled")
class SearchOtherPagesFilterBySubprogramTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        program = PostFactory.create_program(home_page=home_page)

        cls.subprogram1 = PostFactory.create_subprogram(
            program=program,
            subprogram_data={
                'title': 'Gastropod Subprogram',
            },
        )
        cls.subprogram2 = PostFactory.create_subprogram(
            program=program,
            subprogram_data={
                'title': 'Bivalve Subprogram',
            },
        )

        topic_home1 = cls.subprogram1.add_child(
            instance=TopicHomePage(title='Topics')
        )
        cls.topic1 = topic_home1.add_child(
            instance=IssueOrTopic(title='Shells')
        )
        topic_home2 = cls.subprogram2.add_child(
            instance=TopicHomePage(title='Topics')
        )
        cls.topic2 = topic_home2.add_child(
            instance=IssueOrTopic(title='Shells')
        )

    def setUp(self):
        management.call_command('update_index', stdout=StringIO(), chunk_size=50)
        url = f'/api/search/other/?query=shells&subprogram_id={self.subprogram2.pk}'
        self.response = self.client.get(url)
        self.json = self.response.json()

    def test_returns_success_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_returns_exactly_one_result(self):
        self.assertEquals(self.json['count'], 1)
        self.assertEquals(len(self.json['results']), 1)

    def test_returns_correct_response_body(self):
        self.assertEqual(self.json['results'][0]['title'], self.topic2.title)
        self.assertEqual(self.json['results'][0]['id'], self.topic2.pk)


@unittest.skipUnless(TEST_ELASTICSEARCH, "Elasticsearch tests not enabled")
class SearchUpcomingEventsFilterByProgramAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        cls.program1 = PostFactory.create_program(
            home_page=home_page,
            program_data={
                'title': 'Robots Program'
            }
        )
        cls.program2 = PostFactory.create_program(
            home_page=home_page,
            program_data={
                'title': 'Cyborg Program'
            }
        )

        cls.event1 = PostFactory.create_program_content(
            1,
            program=cls.program1,
            content_page_type=ProgramEventsPage,
            post_type=Event,
            content_page_data={},
            post_data={
                'title': 'Party',
                'date': datetime.date.today() + datetime.timedelta(days=1),
            }
        )[0]
        cls.event2 = PostFactory.create_program_content(
            1,
            program=cls.program2,
            content_page_type=ProgramEventsPage,
            post_type=Event,
            content_page_data={},
            post_data={
                'title': 'Party',
                'date': datetime.date.today() + datetime.timedelta(days=1),
            }
        )[0]

        # Some posts that shouldn't be returned in results
        PostFactory.create_program_content(10,
            program=cls.program1,
            content_page_type=ProgramBlogPostsPage,
            post_type=BlogPost,
            post_data={'title': 'Party'}
        )

    def setUp(self):
        management.call_command('update_index', stdout=StringIO(), chunk_size=50)
        url = f'/api/search/upcoming_events/?query=party&program_id={self.program2.pk}'
        self.response = self.client.get(url)
        self.json = self.response.json()

    def test_returns_success_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_returns_exactly_one_person(self):
        self.assertEquals(self.json['count'], 1)
        self.assertEquals(len(self.json['results']), 1)

    def test_returns_correct_response_body(self):
        self.assertEqual(self.json['results'][0]['title'], self.event2.title)
        self.assertEqual(self.json['results'][0]['id'], self.event2.pk)


@unittest.skipUnless(TEST_ELASTICSEARCH, "Elasticsearch tests not enabled")
class SearchUpcomingEventsFilterBySubprogramAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        program = PostFactory.create_program(home_page=home_page)

        cls.subprogram1 = PostFactory.create_subprogram(
            program=program,
            subprogram_data={
                'title': 'Cyborg Program'
            }
        )

        cls.subprogram2 = PostFactory.create_subprogram(
            program=program,
            subprogram_data={
                'title': 'Android Program'
            }
        )
        event_data = {
            'title': 'Party',
            'date': datetime.date.today() + datetime.timedelta(days=1),
        }
        events_home1 = cls.subprogram1.add_child(
            instance=ProgramEventsPage(title='Events')
        )
        events_home2 = cls.subprogram2.add_child(
            instance=ProgramEventsPage(title='Events')
        )
        cls.event1 = events_home1.add_child(instance=Event(**event_data))
        cls.event2 = events_home2.add_child(instance=Event(**event_data))

    def setUp(self):
        management.call_command('update_index', stdout=StringIO(), chunk_size=50)
        url = f'/api/search/upcoming_events/?query=party&subprogram_id={self.subprogram2.pk}'
        self.response = self.client.get(url)
        self.json = self.response.json()

    def test_returns_success_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_returns_exactly_one_person(self):
        self.assertEquals(self.json['count'], 1)
        self.assertEquals(len(self.json['results']), 1)

    def test_returns_correct_response_body(self):
        self.assertEqual(self.json['results'][0]['title'], self.event2.title)
        self.assertEqual(self.json['results'][0]['id'], self.event2.pk)
