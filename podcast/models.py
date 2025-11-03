from home.models import Post

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.embeds.blocks import EmbedBlock
from wagtail.admin.panels import FieldPanel

from newamericadotorg.helpers import paginate_results, get_program_and_subprogram_posts, get_org_wide_posts
from programs.models import AbstractContentPage
from home.models import AbstractHomeContentPage

from django.db import models


class Podcast(Post):
    """
    Podcast class that inherits from the abstract Post
    model and creates pages for Podcasts.
    """
    parent_page_types = ['ProgramPodcastsPage']
    subpage_types = []

    soundcloud = StreamField([
        ('soundcloud_embed', EmbedBlock()),
    ], null=True, blank=True, use_json_field=True)

    itunes_url = models.URLField(blank=True, null=True)

    publication_cover_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    publication_cover_image_alt = models.TextField(
        default='',
        blank=True,
        verbose_name='Publication cover image alternative text',
        help_text='A concise description of the image for users of assistive technology.',
    )

    content_panels = Post.content_panels + [
        FieldPanel('soundcloud'),
        FieldPanel('itunes_url'),
        FieldPanel('publication_cover_image'),
        FieldPanel('publication_cover_image_alt'),
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

    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = ['Podcast']

    @property
    def content_model(self):
        return Podcast

    class Meta:
        verbose_name = "Podcasts Homepage"
