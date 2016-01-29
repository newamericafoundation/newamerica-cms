from django.test import TestCase
from wagtail.tests.utils import WagtailPageTests

from .models import Article, ProgramArticlesPage, AllArticlesHomePage

from programs.models import Program

class ArticleTests(WagtailPageTests):
	def setUp(self):
		Program.objects.create(title='OTI', name='OTI', location=False, depth=3)
		# ProgramArticlesPage.objects.create(title='Articles', depth=4)

	def test_can_create_program_articles_page_under_program(self):
		self.assertCanCreateAt(Program, ProgramArticlesPage)

	def test_can_create_article_under_program_articles_page(self):
		self.assertCanCreateAt(ProgramArticlesPage, Article)

	def test_cant_create_article_under_all_articles_home_page(self):
		self.assertCanNotCreateAt(AllArticlesHomePage, Article)

	# def test_can_create_program_articles_page(self):
	# 	root_page = Program.objects.get(title='OTI')

	# 	self.assertCanCreate(root_page, ProgramArticlesPage, {
	# 		'title': 'Articles',
	# 	})

	def test_can_create_article(self):
		root_page = ProgramArticlesPage.objects.get_or_create(pk=2, depth=4)

		self.assertCanCreate(root_page, Article, {
			'title': 'Article for Testing',
			'date': '01/29/2016',
			'body': 'This is a cool test article!',
		})
