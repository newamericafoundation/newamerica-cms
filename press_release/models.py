from django.db import models

from home.models import Post

from programs.models import Program

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.wagtaildocs.blocks import DocumentChooserBlock

from mysite.pagination import paginate_results


class PressRelease(Post):
    """
    Press Release class that inherits from the abstract
    Post model and creates pages for Press Releases.
    """
    parent_page_types = ['ProgramPressReleasesPage']
    subpage_types = []

    attachment = StreamField([
    	('attachment', DocumentChooserBlock(required=False, null=True)),
    ])

    content_panels = Post.content_panels + [
    	StreamFieldPanel('attachment'),
    ]

    def get_page_type(self):
        type_name = 'press_release'
        return type_name

class AllPressReleasesHomePage(Page):
	"""
	A page which inherits from the abstract Page model and
	returns every Press Release in the PressRelease model
	for the organization-wide Press Release Homepage
	"""
	parent_page_types = ['home.Homepage']
	subpage_types = []

	def get_context(self, request):
		context = super(AllPressReleasesHomePage, self).get_context(request)
		all_posts = PressRelease.objects.all()

		context['all_posts'] = paginate_results(request, all_posts)

		return context

	class Meta:
		verbose_name = "Homepage for all Press Releases"


class ProgramPressReleasesPage(Page):
	"""
	A page which inherits from the abstract Page model and
	returns all Press Releases associated with a specific
	Program which is determined using the url path
	"""
	parent_page_types = ['programs.Program']
	subpage_types = ['PressRelease']

	def get_context(self, request):
		context = super(ProgramPressReleasesPage, self).get_context(request)
		program_slug = request.path.split("/")[-3]
		program = Program.objects.get(slug=program_slug)
		
		all_posts = PressRelease.objects.filter(parent_programs=program)
		context['all_posts'] = paginate_results(request, all_posts)
		
		context['program'] = program

		return context

	class Meta:
		verbose_name = "Press Release Homepage for Program"

