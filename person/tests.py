from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page

from .models import Person, OurPeoplePage

from article.models import ProgramArticlesPage, Article

from home.models import HomePage

from programs.models import Program, Subprogram

class PersonTests(WagtailPageTests):
    """
    Testing functionality of the Person model, 
    including features to associate a Person with
    multiple programs and subprograms,
    """
    def setUp(self):
        self.login()
        self.root_page = Page.objects.get(id=1)
        self.home_page = self.root_page.add_child(instance=HomePage(
            title='New America')
        )
        self.our_people_page = self.home_page.add_child(
            instance=OurPeoplePage(
                title='New America People',
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
        self.program_articles_page = self.program_page.add_child(
            instance=ProgramArticlesPage(title='Program Articles')
        )
        self.article = self.program_articles_page.add_child(
            instance=Article(
                title='Article 1', 
                date='2016-02-02'
            )
        )

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
    def test_article_subpages(self):
        self.assertAllowedSubpageTypes(Article, {})

    def test_program_article_subpages(self):
        self.assertAllowedSubpageTypes(ProgramArticlesPage, {Article})

    def test_all_articles_homepage_subpages(self):
        self.assertAllowedSubpageTypes(AllArticlesHomePage, {})


    # Test you can create a Person object with data
    def test_can_create_person_under_our_people_page(self):
        person = Person(
            title='Sana Javed',
            slug='sana-javed',
            first_name='Sana',
            last_name='Javed',
            role='Central Staff',
            depth=4,
        )
        self.our_people_page.add_child(instance=person)
        self.assertTrue(
            person.get_parent(), 
            self.our_people_page
        )
