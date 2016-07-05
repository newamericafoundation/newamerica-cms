from django.test import TestCase

from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page, Site

from django.test import Client

from .models import Person, OurPeoplePage, PersonProgramRelationship, PersonSubprogramRelationship

from .templatetags.tags import generate_byline

from article.models import ProgramArticlesPage, Article

from home.models import HomePage, PostAuthorRelationship

from programs.models import Program, Subprogram

from django.utils.safestring import mark_safe

from policy_paper.models import AllPolicyPapersHomePage, ProgramPolicyPapersPage, PolicyPaper


class BylineTemplateTagTests(WagtailPageTests):
    def setUp(self):
        self.login()
        site = Site.objects.get()
        page = Page.get_first_root_node()
        home = HomePage(title='New America')
        home_page = page.add_child(instance=home)

        site.root_page = home
        site.save()

        # People objects to test template tags
        # that create byline and determine author order
        program_page_1 = home_page.add_child(
            instance=Program(
                title='OTI',
                name='OTI',
                slug='oti',
                description='OTI',
                location=False,
                depth=3
            )
        )
        program_page_1.save()

        our_people_page = home_page.add_child(
            instance=OurPeoplePage(
                title='Our People',
                depth=3,
            )
        )
        our_people_page.save()

        self.first_person = Person(
            title='First Person',
            slug='first-person',
            first_name='first',
            last_name='person',
            role='Central Staff',
            depth=4,
        )
        our_people_page.add_child(instance=self.first_person)

        self.second_person = Person(
            title='Second Person',
            slug='second-person',
            first_name='Second',
            last_name='Person',
            role='Central Staff',
            depth=4,
        )
        our_people_page.add_child(instance=self.second_person)

        self.third_person = Person(
            title='Third Person',
            slug='third-person',
            first_name='Third',
            last_name='Person',
            role='Central Staff',
            depth=4,
        )
        our_people_page.add_child(instance=self.third_person)

        self.fourth_person = Person(
            title='Fourth Person',
            slug='fourth-person',
            first_name='Fourth',
            last_name='Person',
            role='Central Staff',
            depth=4,
        )
        our_people_page.add_child(instance=self.fourth_person)


        # Using policy papers to test the other post types
        all_policy_papers_home_page = home_page.add_child(
            instance=AllPolicyPapersHomePage(title="Policy Papers")
        )

        program_policy_papers_page = program_page_1.add_child(
            instance=ProgramPolicyPapersPage(title='OTI Policy Papers', slug='oti-policy-papers')
        )
        self.policy_paper = PolicyPaper(
            title='Policy Paper 1',
            slug='policy-paper-1',
            date='2016-06-15',
            depth=5
        )
        program_policy_papers_page.add_child(
            instance=self.policy_paper)
        self.policy_paper.save()


    def test_zero_authors_byline(self):
        authors = self.policy_paper.authors.all()
        actual_response = generate_byline(self.policy_paper.content_type, authors)
        expected_response = mark_safe('')
        self.assertEqual(actual_response, expected_response)

    def test_one_author_byline(self):
        PostAuthorRelationship(author=self.third_person, post=self.policy_paper).save()

        authors = self.policy_paper.authors.all()
        actual_response = generate_byline(self.policy_paper.content_type, authors)
        expected_response = mark_safe('By <a href="/our-people/third-person/">Third Person</a>')
        self.assertEqual(actual_response, expected_response)

    def test_two_authors_byline(self):
        # adding second author relationship to post
        PostAuthorRelationship(author=self.third_person, post=self.policy_paper).save()
        PostAuthorRelationship(author=self.second_person, post=self.policy_paper).save()

        authors = self.policy_paper.authors.all()
        actual_response = generate_byline(self.policy_paper.content_type, authors)
        expected_response = mark_safe('By <a href="/our-people/third-person/">Third Person</a> and <a href="/our-people/second-person/">Second Person</a>')
        self.assertEqual(actual_response, expected_response)

    def test_three_authors_byline(self):
        # adding second and third author relationship to post
        PostAuthorRelationship(author=self.third_person, post=self.policy_paper).save()
        PostAuthorRelationship(author=self.second_person, post=self.policy_paper).save()
        PostAuthorRelationship(author=self.first_person, post=self.policy_paper).save()

        authors = self.policy_paper.authors.all()
        actual_response = generate_byline(self.policy_paper.content_type, authors)
        expected_response = mark_safe('By <a href="/our-people/third-person/">Third Person</a>, <a href="/our-people/second-person/">Second Person</a> and <a href="/our-people/first-person/">First Person</a>')
        self.assertEqual(actual_response, expected_response)

    def test_four_authors_byline(self):
        # adding second and third author relationship to post
        PostAuthorRelationship(author=self.third_person, post=self.policy_paper).save()
        PostAuthorRelationship(author=self.second_person, post=self.policy_paper).save()
        PostAuthorRelationship(author=self.first_person, post=self.policy_paper).save()
        PostAuthorRelationship(author=self.fourth_person, post=self.policy_paper).save()

        authors = self.policy_paper.authors.all()
        actual_response = generate_byline(self.policy_paper.content_type, authors)
        expected_response = mark_safe('By <a href="/our-people/third-person/">Third Person</a>, <a href="/our-people/second-person/">Second Person</a>, <a href="/our-people/first-person/">First Person</a> and <a href="/our-people/fourth-person/">Fourth Person</a>')
        self.assertEqual(actual_response, expected_response)

    def test_two_authors_byline_order(self):
        # adding second author relationship to post
        PostAuthorRelationship(author=self.third_person, post=self.policy_paper).save()
        PostAuthorRelationship(author=self.second_person, post=self.policy_paper).save()
        PostAuthorRelationship.objects.get(author=self.third_person, post=self.policy_paper).delete()
        PostAuthorRelationship(author=self.third_person, post=self.policy_paper).save()

        authors = self.policy_paper.authors.all()
        actual_response = generate_byline(self.policy_paper.content_type, authors)
        expected_response = mark_safe('By <a href="/our-people/second-person/">Second Person</a> and <a href="/our-people/third-person/">Third Person</a>')
        self.assertEqual(actual_response, expected_response)


    def test_podcasts_byline_with_one_author(self):
        PostAuthorRelationship(author=self.third_person, post=self.policy_paper).save()

        authors = self.policy_paper.authors.all()
        actual_response = generate_byline("podcast", authors)
        expected_response = mark_safe('Contributor: <a href="/our-people/third-person/">Third Person</a>')
        self.assertEqual(actual_response, expected_response)


    def test_podcasts_byline_with_multiple_authors(self):
        PostAuthorRelationship(author=self.third_person, post=self.policy_paper).save()
        PostAuthorRelationship(author=self.fourth_person, post=self.policy_paper).save()

        authors = self.policy_paper.authors.all()
        actual_response = generate_byline("podcast", authors)
        expected_response = mark_safe('Contributors: <a href="/our-people/third-person/">Third Person</a> and <a href="/our-people/fourth-person/">Fourth Person</a>')
        self.assertEqual(actual_response, expected_response)

    def test_inthenews_byline(self):
        PostAuthorRelationship(author=self.third_person, post=self.policy_paper).save()

        authors = self.policy_paper.authors.all()
        actual_response = generate_byline("In The News Piece", authors)
        expected_response = mark_safe('In the News: <a href="/our-people/third-person/">Third Person</a>')
        self.assertEqual(actual_response, expected_response)


class PersonTests(WagtailPageTests):
    """
    Testing functionality of the Person model,
    including features to associate a Person with
    multiple programs and subprograms,
    """
    def setUp(self):
        self.login()
        site = Site.objects.get()
        page = Page.get_first_root_node()
        home = HomePage(title='New America')
        self.home_page = page.add_child(instance=home)

        site.root_page = home
        site.save()

        self.our_people_page = self.home_page.add_child(
            instance=OurPeoplePage(
                title='Our People',
                depth=3
            )
        )
        self.program_page = self.home_page.add_child(
            instance=Program(
                title='OTI',
                name='OTI',
                description='OTI',
                location=False,
                depth=3
            )
        )
        self.second_program = self.home_page.add_child(
            instance=Program(
            title='Education',
            name='Education',
            slug='education',
            description='Education',
            location=False,
            depth=3
            )
        )
        self.subprogram_page = self.program_page.add_child(
            instance=Subprogram(
                title='OTI Subprogram',
                name='OTI Subprogram',
                description='OTI Subprogram',
                location=False,
                depth=4
            )
        )
        self.second_subprogram_page = self.program_page.add_child(
            instance=Subprogram(
                title='OTI Subprogram 2',
                name='OTI Subprogram 2',
                description='OTI Subprogram 2',
                location=False,
                depth=4
            )
        )
        self.program_articles_page = self.program_page.add_child(
            instance=ProgramArticlesPage(title='Program Articles')
        )
        self.test_person = Person(
            title='Sana Javed',
            slug='sana-javed',
            first_name='Sana',
            last_name='Javed',
            role='Central Staff',
            depth=4,
        )
        self.our_people_page.add_child(instance=self.test_person)
        self.test_person.save()

        self.article = self.program_articles_page.add_child(
            instance=Article(
                title='Article 1',
                date='2016-02-02'
            )
        )
        PostAuthorRelationship(author=self.test_person, post=self.article).save()

        self.article_2 = self.program_articles_page.add_child(
            instance=Article(
                title='Article 2',
                date='2016-05-02'
            )
        )
        PostAuthorRelationship(author=self.test_person, post=self.article_2).save()


    # Test that a particular child Page type can be created under a
    # parent Page type
    def test_can_create_person_under_correct_parent_page(self):
        self.assertCanCreateAt(
            OurPeoplePage,
            Person
        )

    def test_can_create_our_people_page_under_correct_parent_page(self):
        self.assertCanCreateAt(
            HomePage,
            OurPeoplePage
        )

    def test_cannot_create_person_under_wrong_parent_page(self):
        self.assertCanNotCreateAt(
            HomePage,
            Person
        )

    # Test that the only page types that child model can be created
    # under are parent_models
    def test_person_parent_page(self):
        self.assertAllowedParentPageTypes(
            Person,
            {OurPeoplePage}
        )

    def test_our_people_page_parent_page(self):
        self.assertAllowedParentPageTypes(
            OurPeoplePage,
            {HomePage}
        )

    # Test that the only page types that can be created under
    # parent_model are child_models
    def test_person_page_subpages(self):
        self.assertAllowedSubpageTypes(Person, {})

    def test_our_people_page_subpages(self):
        self.assertAllowedSubpageTypes(OurPeoplePage, {Person})

    # Test you can create a Person object with data
    def test_can_create_person_under_our_people_page(self):
        person = Person(
            title='Foo Bar',
            slug='foo-bar',
            first_name='Foo',
            last_name='Bar',
            role='Central Staff',
            depth=4,
        )
        self.our_people_page.add_child(instance=person)
        self.assertTrue(
            person.get_parent(),
            self.our_people_page
        )

    # Test you can connect a Person and one program
    def test_can_connect_person_to_one_program(self):
        relationship = PersonProgramRelationship.objects.create(
            program=self.program_page,
            person=self.test_person
        )
        relationship.save()
        self.assertIn(self.program_page, self.test_person.belongs_to_these_programs.all())

    # Test you can remove connection between a Person and one program
    def test_removing_connection_between_person_and_one_program(self):
        relationship = PersonProgramRelationship.objects.create(
            program=self.program_page,
            person=self.test_person
        )
        relationship.save()
        relationship.delete()
        self.assertNotIn(self.program_page, self.test_person.belongs_to_these_programs.all())

    # Test you can connect a Person and more than one program
    def test_can_connect_person_to_multiple_programs(self):
        relationship = PersonProgramRelationship.objects.create(
            program=self.program_page,
            person=self.test_person
        )
        relationship.save()
        relationship_two = PersonProgramRelationship.objects.create(
            program=self.second_program,
            person=self.test_person
        )
        relationship_two.save()
        self.assertIn(self.program_page, self.test_person.belongs_to_these_programs.all())
        self.assertIn(self.second_program, self.test_person.belongs_to_these_programs.all())

    # Test you can connect a Person and one subprogram
    def test_can_connect_person_to_one_subprogram(self):
        relationship = PersonSubprogramRelationship.objects.create(
            subprogram=self.subprogram_page,
            person=self.test_person
        )
        relationship.save()
        self.assertIn(self.subprogram_page, self.test_person.belongs_to_these_subprograms.all())

    # Test you can remove connection between a Person and one subprogram
    def test_removing_connection_between_person_and_one_subprogram(self):
        relationship = PersonSubprogramRelationship.objects.create(
            subprogram=self.subprogram_page,
            person=self.test_person
        )
        relationship.save()
        relationship.delete()
        self.assertNotIn(self.subprogram_page, self.test_person.belongs_to_these_subprograms.all())

    # Test you can connect a Person and more than one subprogram
    def test_can_connect_person_to_multiple_subprograms(self):
        relationship = PersonSubprogramRelationship.objects.create(
            subprogram=self.subprogram_page,
            person=self.test_person
        )
        relationship.save()
        relationship_two = PersonSubprogramRelationship.objects.create(
            subprogram=self.second_subprogram_page,
            person=self.test_person
        )
        relationship_two.save()
        self.assertIn(self.subprogram_page, self.test_person.belongs_to_these_subprograms.all())
        self.assertIn(self.second_subprogram_page, self.test_person.belongs_to_these_subprograms.all())

    # Test you can add featured work to a person's bio page
    def test_adding_feature_work_item_to_person_bio(self):
        self.test_person.feature_work_1 = self.article
        self.assertEqual(self.article, self.test_person.feature_work_1)

        self.test_person.feature_work_1 = self.article_2
        self.assertEqual(self.article_2, self.test_person.feature_work_1)

    # Test you can add set a person to be listed as an expert
    def test_setting_person_as_expert(self):
        self.test_person.expert = True
        self.assertEqual(True, self.test_person.expert)
        self.test_person.expert = False
        self.assertEqual(False, self.test_person.expert)

    # Test you can add set a person to be listed as part of leadership
    def test_setting_person_as_leadership(self):
        self.test_person.leadership = True
        self.assertEqual(True, self.test_person.leadership)

        self.test_person.leadership = False
        self.assertEqual(False, self.test_person.leadership)

    # Test you can change a person's role
    def test_changing_person_role(self):
        self.test_person.role = 'Program Staff'
        self.assertEqual('Program Staff', self.test_person.role)
        self.assertNotEqual('Central Staff', self.test_person.role)

    # Test a person page has their conent
    def test_person_page_has_their_conent(self):
        c = Client()
        response = c.get('/our-people/sana-javed/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 2)

    # Test a person page has content ordered by date
    def test_person_page_has_content_ordered_by_date(self):
        c = Client()
        response = c.get('/our-people/sana-javed/', follow=True)
        self.assertEqual(response.status_code, 200)
        post_titles = []
        for post in response.context['posts']:
            post_titles.append(post.title)
        self.assertEqual(post_titles, ['Article 2', 'Article 1'])

    # Test that the second page of the person bio page has no bio and only content results
    def test_second_person_page_of_bio_has_no_bio_only_content_results(self):
        pass



