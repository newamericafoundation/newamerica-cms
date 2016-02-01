from django.test import TestCase

from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page

from .models import Article, ProgramArticlesPage, AllArticlesHomePage

from home.models import HomePage

from programs.models import Program

class ArticleTests(WagtailPageTests):
	def setUp(self):
		self.root_page = Page.objects.get(id=1)
		self.home_page = self.root_page.add_child(instance=HomePage(title='New America'))
		self.program_page = self.home_page.add_child(instance=Program(title='OTI', name='OTI', location=False, depth=3))
		self.login()

	
	"""
	Testing whether a particular child Page type can be created or can not be 
	created under certain parent Page types
	"""
	def test_can_create_program_articles_page_under_program(self):
		self.assertCanCreateAt(Program, ProgramArticlesPage)

	def test_can_create_article_under_program_articles_page(self):
		self.assertCanCreateAt(ProgramArticlesPage, Article)

	def test_cant_create_article_under_all_articles_home_page(self):
		self.assertCanNotCreateAt(AllArticlesHomePage, Article)


	"""
	Testing whether a child of the given Page type can be created
	under the parent with the supplied POST data
	"""
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

	def test_can_create_article_under_program(self):
		self.program_articles_page = self.program_page.add_child(instance=ProgramArticlesPage(title='Articles'))
		self.assertCanCreate(self.program_articles_page, Article, {
			'title':'Test Article 1',
			'date':'2016-02-01',
			'body-count':0,
			}
		)



