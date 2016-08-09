from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page, Site

from django.test import Client

from .models import Person, OurPeoplePage, PersonProgramRelationship, PersonSubprogramRelationship

from article.models import ProgramArticlesPage, Article

from home.models import HomePage, PostAuthorRelationship

from programs.models import Program, Subprogram

from django.utils.safestring import mark_safe

from policy_paper.models import AllPolicyPapersHomePage, ProgramPolicyPapersPage, PolicyPaper


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



