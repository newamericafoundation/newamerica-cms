from django.test import TestCase

from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page

from .models import Article, ProgramArticlesPage, AllArticlesHomePage

from home.models import HomePage

from programs.models import Program

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
		self.home_page = self.root_page.add_child(instance=HomePage(title='New America'))
		self.program_page = self.home_page.add_child(instance=Program(title='OTI', name='OTI', location=False, depth=3))
		self.program_articles_page = self.program_page.add_child(instance=ProgramArticlesPage(title='Program Articles'))
		self.article = self.program_articles_page.add_child(instance=Article(title='Article 1', date='2016-02-02'))

	def test_can_create_program_articles_page_under_program(self):
		self.assertCanCreateAt(Program, ProgramArticlesPage)

	def test_can_create_article_under_program_articles_page(self):
		self.assertCanCreateAt(ProgramArticlesPage, Article)

	def test_cant_create_article_under_all_articles_home_page(self):
		self.assertCanNotCreateAt(AllArticlesHomePage, Article)


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

	def test_article_is_inside_program(self):
		


