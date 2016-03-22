from django.db import models

from home.models import Post

from wagtail.wagtailcore.models import Page

from programs.models import Program

from person.models import Person

from mysite.pagination import paginate_results


class BlogPost(Post):
	"""
	Blog class that inherits from the abstract
	Post model and creates pages for blog posts.
	"""
	parent_page_types = ['ProgramBlogPostsPage']
	subpage_types = []


class AllBlogPostsHomePage(Page):
	"""
	A page which inherits from the abstract Page model and 
	returns every Blog post in the BlogPost model for the 
	Blog posts homepage
	"""
	parent_page_types = ['home.HomePage', ]
	subpage_types = []

	def get_context(self, request):
		context = super(AllBlogPostsHomePage, self).get_context(request)
		
		all_posts = BlogPost.objects.all()

		context['all_posts'] = paginate_results(request, all_posts)

		return context

	class Meta:
		verbose_name = "Homepage for all Blog Posts"


class ProgramBlogPostsPage(Page):
	"""
	A page which inherits from the abstract Page model and returns
	all Blog Posts associated with a specific program which is 
	determined using the url path
	"""

	parent_page_types = ['programs.Program',]
	subpage_types = ['BlogPost']

	def get_context(self, request):
		context = super(ProgramBlogPostsPage, self).get_context(request)
		program_slug = request.path.split("/")[-3]
		program = Program.objects.get(slug=program_slug)

		all_posts = BlogPost.objects.filter(parent_programs=program)
		context['all_posts'] = paginate_results(request, all_posts)
		
		context['program'] = program
		return context
		

	class Meta:
		verbose_name = "Blog Homepage for Program"
