from django.db import models

from home.models import Post

from programs.models import Program

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel


class Quoted(Post):
    """
    Quoted class that inherits from the abstract
    Post model and creates pages for Quoted pages
    where New America was in the news.
    """
    parent_page_types = ['ProgramQuotedPage']
    subpage_types = []

    source = models.TextField(max_length=8000)
    source_url = models.URLField()

    content_panels = Post.content_panels + [
    	FieldPanel('source'),
    	FieldPanel('source_url'),
    ]


class AllQuotedHomePage(Page):
	"""
	A page which inherits from the abstract Page model and
	returns every Quoted piece from the Quoted model
	for the organization-wide Quoted Homepage 
	"""
	parent_page_types = ['home.Homepage']
	subpage_types = []

	def get_context(self, request):
		context = super(AllQuotedHomePage, self).get_context(request)
		context['quoted_pieces'] = Quoted.objects.all()

		return context
	class Meta:
		verbose_name = "Homepage for all Quoted Pieces (formerly In The News)"


class ProgramQuotedPage(Page):
	parent_page_types = ['programs.Program']
	subpage_types = ['Quoted']

	def get_context(self, request):
		context = super(ProgramQuotedPage, self).get_context(request)
		program_slug = request.path.split("/")[-3]
		program = Program.objects.get(slug=program_slug)
		context['quoted_pieces'] = Quoted.objects.filter(parent_programs=program)
		context['program'] = program

		return context
	class Meta:
		verbose_name = "Quoted Homepage for Programs (formerly In The News)"
