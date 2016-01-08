from django.db import models

from home.models import Post

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.wagtailcore.blocks import URLBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock

from programs.models import Program

class PolicyPaper(Post):
    """
    Policy paper class that inherits from the abstract
    Post model and creates pages for Policy Papers.
    """
    parent_page_types = ['ProgramPolicyPapersPage']
    subpage_types = []

    excerpt = models.TextField()

    paper_url = StreamField([
    	('policy_paper_url', URLBlock(required=False, null=True)),
    ])

    attachment = StreamField([
    	('attachment', DocumentChooserBlock(required=False, null=True)),
    ])

    content_panels = Post.content_panels + [
    	FieldPanel('excerpt'),
    	StreamFieldPanel('paper_url'),
    	StreamFieldPanel('attachment'),
    ]


class AllPolicyPapersHomePage(Page):
	"""
	A page which inherits from the abstract Page model and
	returns every Policy Paper in the Policy Paper model
	for the organization wide Policy Paper Homepage
	"""
	parent_page_types = ['home.Homepage']
	subpage_types = []

	def get_context(self, request):
		context = super(AllPolicyPapersHomePage, self).get_context(request)
		context['policy_papers'] = PolicyPaper.objects.all()

		return context

	class Meta:
		verbose_name = "Homepage for all Policy Papers"


class ProgramPolicyPapersPage(Page):
	"""
	A page which inherits from the abstract Page model and
	returns all Policy Papers associated with a specific
	Program which is determined using the url path
	"""
	parent_page_types = ['programs.Program']
	subpage_types = ['PolicyPaper']

	def get_context(self, request):
		context = super(ProgramPolicyPapersPage, self).get_context(request)
		program_slug = request.path.split("/")[-3]
		program = Program.objects.get(slug=program_slug)
		context['policy_papers'] = PolicyPaper.objects.filter(parent_programs=program)
		context['program'] = program

		return context

	class Meta:
		verbose_name = "Policy Paper Homepage for Programs"
