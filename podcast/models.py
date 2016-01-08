from django.db import models

from home.models import Post

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel

from programs.models import Program


class Podcast(Post):
    """
    Podcast class that inherits from the abstract Post
    model and creates pages for Podcasts.
    """
    parent_page_types = ['ProgramPodcastsPage']
    subpage_types = []

    soundcloud = StreamField([
    	('soundcloud_embed', EmbedBlock()),
    
    ])

    content_panels = Post.content_panels + [
    	StreamFieldPanel('soundcloud'),

    ]


class AllPodcastsHomePage(Page):
	"""
	A page which inherits from the abstract Page model
	and returns every Podcast in the Podcast model for
	the organization wide Podcast homepage
	"""

	parent_page_types = ['home.HomePage',]
	subpage_types = []

	def get_context(self, request):
		context = super(AllPodcastsHomePage, self).get_context(request)
		context['podcasts'] = Podcast.objects.all()

		return context

	class Meta:
		verbose_name = "Homepage for all Podcasts"


class ProgramPodcastsPage(Page):
	"""
	A page which inherits from the abstract Page model and
	returns all Podcasts associated with a sepcific program
	which is determined using the url path
	"""

	parent_page_types = ['programs.Program']
	subpage_types = ['Podcast']

	def get_context(self, request):
		context = super(ProgramPodcastsPage, self).get_context(request)
		program_slug = request.path.split("/")[-3]
		program = Program.objects.get(slug=program_slug)
		context['podcasts'] = Podcast.objects.filter(parent_programs=program)
		context['program'] = program
		return context

	class Meta:
		verbose_name = "Podcast Homepage for Program"

