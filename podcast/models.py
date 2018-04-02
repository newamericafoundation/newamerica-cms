from home.models import Post

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel

from newamericadotorg.helpers import paginate_results, get_program_and_subprogram_posts, get_org_wide_posts
from programs.models import AbstractContentPage
from home.models import AbstractHomeContentPage

from django.db import models


class Podcast(Post):
    """
    Podcast class that inherits from the abstract Post
    model and creates pages for Podcasts.
    """
    parent_page_types = ['ProgramPodcastsPage', 'programs.BlogProject', 'programs.BlogSeries']
    subpage_types = []

    soundcloud = StreamField([
        ('soundcloud_embed', EmbedBlock()),
    ])

    itunes_url = models.URLField(blank=True, null=True)

    content_panels = Post.content_panels + [
        StreamFieldPanel('soundcloud'),
        FieldPanel('itunes_url'),
    ]

    class Meta:
        verbose_name = 'Podcast'


class AllPodcastsHomePage(AbstractHomeContentPage):
    """
    A page which inherits from the abstract Page model
    and returns every Podcast in the Podcast model for
    the organization wide Podcast homepage
    """

    parent_page_types = ['home.HomePage']
    subpage_types = []

    def get_context(self, request):
        return get_org_wide_posts(
            self,
            request,
            AllPodcastsHomePage,
            Podcast
        )

    @property
    def content_model(self):
        return Podcast

    class Meta:
        verbose_name = "Homepage for all Podcasts"


class ProgramPodcastsPage(AbstractContentPage):
    """
    A page which inherits from the abstract Page model and
    returns all Podcasts associated with a sepcific program
    or Subprogram
    """

    parent_page_types = ['programs.Program', 'programs.Subprogram']
    subpage_types = ['Podcast']

    def get_context(self, request):
        return get_program_and_subprogram_posts(
            self,
            request,
            ProgramPodcastsPage,
            Podcast
        )

    @property
    def content_model(self):
        return Podcast

    class Meta:
        verbose_name = "Podcasts Homepage"
