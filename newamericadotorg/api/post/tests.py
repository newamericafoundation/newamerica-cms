from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from wagtail.core.models import Page, Site

from test_factories import PostFactory

from person.models import Person
from home.models import HomePage, CustomImage, PostAuthorRelationship
from programs.models import Program
from blog.models import ProgramBlogPostsPage, BlogPost
from other_content.models import OtherPost, ProgramOtherPostsPage, OtherPostCategory
from report.models import Report, ReportsHomepage
from policy_paper.models import PolicyPaper, ProgramPolicyPapersPage
from in_depth.models import InDepthProject, AllInDepthHomePage

class PostAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        program = PostFactory.create_program(home_page=home_page)

        indepthpage = home_page.add_child(instance=AllInDepthHomePage(
            title='In Depth Home Page'
        ))

        indepthpage.add_child(instance=InDepthProject(
            title="In Depth Project",
            date=str(date.today())
        ))
        indepthpage.add_child(instance=InDepthProject(
            title="In Depth Project 2: same date, different id",
            date=str(date.today())
        ))
        for post in InDepthProject.objects.all():
            post.save()

        PostFactory.create_program_content(5,
            program=program,
            content_page_type=ProgramOtherPostsPage,
            post_type=OtherPost,
            content_page_data={'singular_title': 'Test Content', 'title': 'Test Contents'}
        )
        for post in OtherPost.objects.all():
            post.save()

        PostFactory.create_program_content(5,
            program=program,
            content_page_type=ProgramBlogPostsPage,
            post_type=BlogPost
        )
        for post in BlogPost.objects.all():
            post.save()

        PostFactory.create_program_content(5,
            program=program,
            content_page_type=ProgramPolicyPapersPage,
            post_type=PolicyPaper
        )
        for post in PolicyPaper.objects.all():
            post.save()


        PostFactory.create_program_content(5,
            program=program,
            content_page_type=ReportsHomepage,
            post_type=Report
        )
        for post in Report.objects.all():
            post.save()


    def test_get_list(self):
        url = '/api/post/'
        response = self.client.get(url)

        self.assertEqual(len(response.json()['results']), 22)

    def test_get_reports(self):
        url = '/api/post/?content_type=report'
        response = self.client.get(url)

        self.assertEqual(len(response.json()['results']), 12)

    def test_other_content_by_title(self):
        url = '/api/post/?other_content_type_title=Test%20Contents'
        response = self.client.get(url)

        self.assertEqual(len(response.json()['results']), 5)

    def test_other_content_by_title_and_category(self):
        other_content_page = ProgramOtherPostsPage.objects.first()
        category = other_content_page.add_child(instance=OtherPostCategory(
            title='Foo'
        ))

        category.save()

        post = category.add_child(instance=OtherPost(
            **PostFactory.post_data()
        ))

        post.save()

        url = '/api/post/?other_content_type_title=Test%20Contents&category=Foo'
        response = self.client.get(url)

        self.assertEqual(len(response.json()['results']), 1)

    def test_author_serialization(self):
        blog_post = BlogPost.objects.first()
        author1 = PostFactory.create_person(
            person_data={
                'title': 'Albert Zeta',
                'first_name': 'Albert',
                'last_name': 'Zeta'
            }
        )
        author2 = PostFactory.create_person(
            person_data={
                'title': 'Albert Alpha',
                'first_name': 'Albert',
                'last_name': 'Alpha'
            }
        )

        author_rel1 = PostAuthorRelationship(
            author=author1,
            post=blog_post
        )

        author_rel1.save()

        author_rel2 = PostAuthorRelationship(
            author=author2,
            post=blog_post
        )

        author_rel2.save()

        blog_post = BlogPost.objects.first()

        url = '/api/post/?id=%s' % str(blog_post.id)
        response = self.client.get(url)
        results = response.json()['results']

        # order should be the order that they were saved
        self.assertEqual(results[0]['authors'][0]['last_name'], 'Zeta')

    def test_image_serialization(self):
        blog_post = BlogPost.objects.first()

        img = PostFactory.create_image('img.png')
        img_file = SimpleUploadedFile('fake_image.png', img.getvalue())
        custom_image = CustomImage(file=img_file)
        custom_image.save()

        blog_post.story_image = custom_image
        blog_post.save()

        url = '/api/post/?id=%s&story_image_rendition=small' % str(blog_post.id)
        response = self.client.get(url)
        result = response.json()['results'][0]

        self.assertTrue('fill-300x230' in result['story_image'])

    def test_post_ordering(self):
        url = '/api/post/'
        response = self.client.get(url)
        results = response.json()['results']

        results_sorted_by_id = sorted(results, key=lambda post: post['id'], reverse=True)

        self.assertEqual(
            results,
            sorted(results_sorted_by_id, key=lambda post: post['date'], reverse=True)
        )
