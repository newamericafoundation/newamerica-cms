from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from home.models import Post
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.contrib.table_block.blocks import TableBlock

from newamericadotorg.blocks import ButtonBlock, IframeBlock, DatavizBlock
from .blocks import CollapsibleBlock, PanelColorThemes, PanelBody

from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from newamericadotorg.helpers import paginate_results, get_org_wide_posts

class InDepthSection(Page):
    """

    """
    parent_page_types = ['InDepthProject']
    subpage_types = []

    subheading = RichTextField(blank=True, null=True)
    generate_title_panel = models.BooleanField(default=False, help_text="Will create a title panel before the first panel if checked")

    panels = StreamField([
        ('panel',
            blocks.StructBlock([
            	('panel_title', blocks.CharBlock(required=True)),
            	('panel_color_theme', PanelColorThemes()),
            	('panel_body', PanelBody())
            ])
        )
    ], null=True, blank=True)

    story_excerpt = models.CharField(blank=True, null=True, max_length=140)

    story_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('subheading'),
        FieldPanel('generate_title_panel'),
        StreamFieldPanel('panels'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('story_excerpt'),
        ImageChooserPanel('story_image'),
    ]

    def get_context(self, request):
        context = super(InDepthSection, self).get_context(request)
        project_root = self.get_parent()
        context['project_root'] = project_root
        context['authors'] = project_root.specific.authors.order_by('pk')
        siblings = self.get_siblings(inclusive=True).live()
        index = 0
        for i, item in enumerate(siblings):
            if (item.title == self.title):
                index = i

        context['index'] = index
        context['siblings'] = siblings
        if (index != 0):
            context['previous_sibling'] = siblings[(index - 1)]
        if (index != len(siblings) - 1):
            context['next_sibling'] = siblings[(index + 1)]

        return context

    class Meta:
        verbose_name = "In-Depth Project Section"


class InDepthProject(Post):
    """

    """
    parent_page_types = ['AllInDepthHomePage']
    subpage_types = ['InDepthSection']

    about_the_project = RichTextField(blank=True, null=True)

    buttons = StreamField([
        ('button',
            blocks.StructBlock([
            	('button_text', blocks.CharBlock(required=True, max_length=50)),
            	('button_url', blocks.URLBlock(required=True, default="https://www.")),
            ])
        )
    ], null=True, blank=True)

    project_logo = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    project_logo_link = models.URLField(blank=True, null=True, max_length=140)

    show_data_download_links = models.BooleanField(default=True)

    content_panels = Post.content_panels + [
        FieldPanel('about_the_project'),
    	StreamFieldPanel('buttons'),
        ImageChooserPanel('project_logo'),
        FieldPanel('project_logo_link'),
        FieldPanel('show_data_download_links'),
    ]

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "In-Depth Project"


class AllInDepthHomePage(Page):
    """
    A page which inherits from the abstract Page model and
    returns every In Depth Page
    """
    parent_page_types = ['home.HomePage', ]
    subpage_types = ['InDepthProject']

    story_excerpt = models.CharField(blank=True, null=True, max_length=140)

    story_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    promote_panels = Page.promote_panels + [
        FieldPanel('story_excerpt'),
        ImageChooserPanel('story_image'),
    ]

    def get_context(self, request):
        return get_org_wide_posts(
            self,
            request,
            AllInDepthHomePage,
            InDepthProject
        )

    class Meta:
        verbose_name = "Homepage for all In-Depth Projects"
