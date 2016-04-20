from django.test import TestCase

from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page

from .models import Article, ProgramArticlesPage, AllArticlesHomePage

from home.models import HomePage, PostProgramRelationship

from programs.models import Program, Subprogram

class ArticleTests(WagtailPageTests):
    """
    Testing hierarchies between pages and whether it is possible 
    to create an All Articles Homepage under the Homepage, 
    a Program Articles Page under Program pages, Articles under 
    Program Articles Pages. 

    Testing the many to many relationships between Programs and Articles. 
    """
    
    def setUp(self):
        self.login()
        self.root_page = Page.objects.get(id=1)
        self.home_page = self.root_page.add_child(instance=HomePage(
            title='New America')
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
        self.program_articles_page = self.program_page.add_child(
            instance=ProgramArticlesPage(title='Program Articles')
        )
        self.article = self.program_articles_page.add_child(instance=Article(title='Article 1', date='2016-02-02'))


    #Test that a particular child Page type can be created under a parent Page type
    def test_can_create_program_articles_page_under_program(self):
        self.assertCanCreateAt(Program, ProgramArticlesPage)

    def test_can_create_article_under_program_articles_page(self):
        self.assertCanCreateAt(ProgramArticlesPage, Article)

    def test_cant_create_article_under_all_articles_home_page(self):
        self.assertCanNotCreateAt(AllArticlesHomePage, Article)


    #Test that the only page types that child_model can be created under are parent_models
    def test_article_parent_page(self):
        self.assertAllowedParentPageTypes(Article, {ProgramArticlesPage})

    def test_program_article_parent_page(self):
        self.assertAllowedParentPageTypes(ProgramArticlesPage, {Program, Subprogram})

    def test_all_articles_homepage_parent_page(self):
        self.assertAllowedParentPageTypes(AllArticlesHomePage, {HomePage})


    #Test that the only page types that can be created under parent_model are child_models
    def test_article_subpages(self):
        self.assertAllowedSubpageTypes(Article, {})

    def test_program_article_subpages(self):
        self.assertAllowedSubpageTypes(ProgramArticlesPage, {Article})

    def test_all_articles_homepage_subpages(self):
        self.assertAllowedSubpageTypes(AllArticlesHomePage, {})


    #Test that pages can be created with POST data
    def test_can_create_all_articles_homepage_under_homepage(self):
        self.assertCanCreate(self.home_page, AllArticlesHomePage, {
            'title':'Articles',
            }
        )

    def test_can_create_program_articles_page(self):
        self.assertCanCreate(self.program_page, ProgramArticlesPage, {
            'title':'Articles',
            }
        )


    # Test relationship between article and one parent Program
    def test_article_has_relationship_to_one_program(self):
        article = Article.objects.all()[0]
        self.assertEqual(article.parent_programs.all()[0].title, 'OTI')


    # Test relationship between article and two parent Programs
    def test_article_has_relationship_to_two_programs(self):
        article = Article.objects.all()[0]
        relationship, created = PostProgramRelationship.objects.get_or_create(program=self.second_program, post=article)
        relationship.save()
        self.assertEqual(article.parent_programs.all()[0].title, 'Education')


    # Test you can delete an article attached to one Program
    def test_can_delete_blog_post_with_one_program(self):
        article = Article.objects.first()
        article.delete()
        self.assertEqual(Article.objects.filter(title='Article 1').first(), None)
        self.assertNotIn(article, ProgramArticlesPage.objects.filter(title='Program Articles').first().get_children())
        self.assertEqual(PostProgramRelationship.objects.filter(post=article).first(), None)
        self.assertEqual(PostProgramRelationship.objects.filter(post=article, program=self.program_page).first(), None)

    # Test article can be deleted if attached to two Programs
    def test_can_delete_blog_post_with_two_programs(self):
        article = Article.objects.first()
        relationship, created = PostProgramRelationship.objects.get_or_create(post=article, program=self.second_program)
        if created:
            relationship.save()
        article.delete()
        self.assertEqual(Article.objects.filter(title='Article 1').first(), None)
        self.assertNotIn(article, ProgramArticlesPage.objects.filter(title='Program Articles').first().get_children())
        self.assertEqual(PostProgramRelationship.objects.filter(post=article, program=self.program_page).first(), None)
        self.assertEqual(PostProgramRelationship.objects.filter(post=article, program=self.second_program).first(), None)