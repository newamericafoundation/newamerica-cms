from django.test import TestCase

from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page

from .models import BlogPost, AllBlogPostsHomePage, ProgramBlogPostsPage

from home.models import HomePage, PostProgramRelationship

from programs.models import Program

class BlogPostTests(WagtailPageTests):
	"""
	Testing the BlogPost, AllBlogPostsHomePage, and
	ProgramBlogPostsPage models to confirm hierarchies
	between pages and whether it is possible to create
	pages where it is appropriate.

	"""

	def setUp(self):
		self.login()
		self.root_page = Page.objects.get(id=1)
		self.home_page = self.root_page.add_child(instance=HomePage(title='New America'))
		self.program_page_1 = self.home_page.add_child(instance=Program(title='OTI', name='OTI', location=False, depth=3))
		self.program_blog_posts_page = self.program_page_1.add_child(instance=ProgramBlogPostsPage(title='OTI Blog'))
		self.blog_post = self.program_blog_posts_page.add_child(instance=BlogPost(title='Blog Post 1', date='2016-02-10'))


	# Test that a particular child Page can be created under 
	# the appropriate parent Page 
	def test_can_create_blog_post_under_program_blog_posts_page(self):
		self.assertCanCreateAt(ProgramBlogPostsPage, BlogPost)

	def test_cannot_create_blog_post_under_all_blog_posts_page(self):
		self.assertCanNotCreateAt(AllBlogPostsHomePage, BlogPost)

	def test_can_create_program_blog_posts_page_under_program(self):
		self.assertCanCreateAt(Program, ProgramBlogPostsPage)


	# Test allowed parent page types
	def test_blog_post_parent_page(self):
		self.assertAllowedParentPageTypes(BlogPost, {ProgramBlogPostsPage})

	def test_program_blog_post_parent_page(self):
		self.assertAllowedParentPageTypes(ProgramBlogPostsPage, {Program})

	def test_all_blog_posts_parent_page(self):
		self.assertAllowedParentPageTypes(AllBlogPostsHomePage, {HomePage})


	# Test allowed subpage types
	def test_blog_post_subpages(self):
		self.assertAllowedSubpageTypes(BlogPost, {})

	def test_program_blog_post_subpages(self):
		self.assertAllowedSubpageTypes(ProgramBlogPostsPage, {BlogPost})
	
	def test_all_blog_post_subpages(self):
		self.assertAllowedSubpageTypes(AllBlogPostsHomePage, {})

	#Test that pages can be created with POST data
	def test_can_create_all_blog_post_page_under_homepage(self):
		self.assertCanCreate(self.home_page, AllBlogPostsHomePage, {
			'title':'All Blogs Posts',
			}
		)

	def test_can_create_program_blog_posts_page(self):
		self.assertCanCreate(self.program_page_1, ProgramBlogPostsPage, {
			'title':'Program Blogs',
			}
		)


	# Test relationship between BlogPost and one parent Program
	def test_blog_post_has_relationship_to_one_program(self):
		blog = BlogPost.objects.first()
		self.assertEqual(blog.parent_programs.all()[0].title, 'OTI')


	# Test you can create a BlogPost with two parent Programs
	def test_blog_post_has_relationship_to_two_parent_programs(self):
		blog = BlogPost.objects.first()
		second_program = Program.objects.create(title='Education', name='Education', location=False, depth=3)
		relationship, created = PostProgramRelationship.objects.get_or_create(program=second_program, post=blog)
		relationship.save()
		self.assertEqual(blog.parent_programs.filter(title='Education').first().title, 'Education')


	# Test blog post can be deleted if BlogPost attached to one Program
	def test_can_delete_blog_post_with_one_program(self):
		blog = BlogPost.objects.first()
		blog.delete()
		self.assertEqual(BlogPost.objects.filter(title='Blog Post 1').first(), None)
		self.assertNotIn(blog, ProgramBlogPostsPage.objects.filter(title='OTI Blog').first().get_children())
		self.assertEqual(PostProgramRelationship.objects.filter(post=blog).first(), None)
		self.assertEqual(PostProgramRelationship.objects.filter(post=blog, program=self.program_page_1).first(), None)


	# Test blog post can be deleted if attached to two Programs
	def test_can_delete_blog_post_with_two_programs(self):
		blog = BlogPost.objects.first()
		second_program = Program.objects.create(title='Education', name='Education', location=False, depth=3)
		relationship, created = PostProgramRelationship.objects.get_or_create(program=second_program, post=blog)
		if created:
			relationship.save()
		blog.delete()
		self.assertEqual(BlogPost.objects.filter(title='Blog Post 1').first(), None)
		self.assertNotIn(blog, ProgramBlogPostsPage.objects.filter(title='OTI Blog').first().get_children())
		self.assertEqual(PostProgramRelationship.objects.filter(post=blog, program=self.program_page_1).first(), None)
		self.assertEqual(PostProgramRelationship.objects.filter(post=blog, program=second_program).first(), None)
