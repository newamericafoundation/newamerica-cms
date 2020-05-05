from io import BytesIO

from django.utils.text import slugify
from PIL import Image

from wagtail.core.models import Page, Site

from home.models import Post, HomePage
from programs.models import Program, Subprogram
from person.models import Person, OurPeoplePage
from issue.models import IssueOrTopic, TopicHomePage
from conference.models import Conference

from report.models import Report
from article.models import Article
from blog.models import BlogPost
from book.models import Book
from event.models import Event
from in_depth.models import InDepthProject
from other_content.models import OtherPost
from podcast.models import Podcast
from policy_paper.models import PolicyPaper
from press_release.models import PressRelease
from quoted.models import Quoted
from weekly.models import WeeklyArticle, WeeklyEdition

from faker import Faker
fake = Faker()

class PostFactory():
    @staticmethod
    def post_data(**kwargs):
        date = '%s-%s-01' % (fake.year(), fake.month())

        args = {
            'title': fake.text(max_nb_chars=15),
            'date': date,
            'slug': slugify(' '.join(fake.words())),
            'story_excerpt': fake.text(max_nb_chars=140)
        }

        return { **args, **kwargs }

    @staticmethod
    def program_data(**kwargs):
        args = {
            'title': fake.company(),
            'name': fake.company(),
            'slug': slugify(fake.words()),
            'description': fake.words(),
            'depth': 3,
            'show_in_menus': True
        }

        return { **args, **kwargs }

    @staticmethod
    def page_data(**kwargs):
        args = {
            'title': fake.text(max_nb_chars=15)
        }

        return { **args, **kwargs }

    @staticmethod
    def person_data(**kwargs):
        args = {
            'title': fake.text(max_nb_chars=15),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'role': 'Program Staff'
        }

        return { **args, **kwargs }

    @staticmethod
    def create_homepage():
        site = Site.objects.get()
        page = Page.get_first_root_node()
        home = HomePage(title='New America')
        home_page = page.add_child(instance=home)

        site.root_page = home
        site.save()

        return home_page

    @staticmethod
    def create_content(n, content_page, post_type, post_data={}):
        content = []
        for i in range(n):
            post = content_page.add_child(instance=post_type(
                **PostFactory.post_data(**post_data)
            ))

            content.append(post)

        return content

    @staticmethod
    def create_program_content_page(program, content_page_type, content_page_data={}):
        return program.add_child(instance=content_page_type(
            **PostFactory.page_data(**content_page_data)
        ))

    @staticmethod
    def create_program_content(n, program, content_page_type, post_type, content_page_data={}, post_data={} ):
        content_page = program.add_child(instance=content_page_type(
            **PostFactory.page_data(**content_page_data)
        ))

        content = []
        for i in range(n):
            post = content_page.add_child(instance=post_type(
                **PostFactory.post_data(**post_data)
            ))

            content.append(post)

        return content

    @staticmethod
    def create_program(home_page, program_data={}):
        program = home_page.add_child(instance=Program(
            **PostFactory.program_data(**program_data)
        ))

        return program

    @staticmethod
    def create_subprogram(program, subprogram_data={}):
        subprogram = program.add_child(instance=Subprogram(
            **PostFactory.program_data(**subprogram_data)
        ))

        return subprogram

    @staticmethod
    def create_person(person_data={}):
        people_page = OurPeoplePage.objects.first()
        if people_page == None:
            home_page = HomePage.objects.first()
            people_page = home_page.add_child(instance=OurPeoplePage(
                title='Our People'
            ))

        person = people_page.add_child(instance=Person(
            **PostFactory.person_data(**person_data)
        ))

        return person

    @staticmethod
    def create_image(filename, size=(100, 100), image_mode='RGB', image_format='PNG'):

        data = BytesIO()
        Image.new(image_mode, size).save(data, image_format)
        data.seek(0)

        return data

    @staticmethod
    def create_program_topics(n, program, topic_home_data={}, topic_data={}):

        topic_home = program.add_child(instance=TopicHomePage(
            **PostFactory.page_data(**topic_home_data)
        ))

        topics = []
        for i in range(n):
            topic = topic_home.add_child(instance=IssueOrTopic(
                **PostFactory.page_data(**topic_data)
            ))

            topics.append(topic)

        return topics

    @staticmethod
    def create_subtopics(n, parent_topic, topic_data={}):

        topics = []
        for i in range(n):
            topic = parent_topic.add_child(instance=IssueOrTopic(
                **PostFactory.page_data(**topic_data)
            ))

            topics.append(topic)

        return topics
