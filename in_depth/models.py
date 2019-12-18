from __future__ import unicode_literals

from django.db import models
import json

from wagtail.core.models import Page
from home.models import Post
from wagtail.core import blocks
from wagtail.core.fields import StreamField, RichTextField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.contrib.table_block.blocks import TableBlock

from newamericadotorg.blocks import ButtonBlock, IframeBlock, DatavizBlock
from .blocks import CollapsibleBlock, PanelColorThemes, PanelBody, DataReferenceBlock, VideoDataReferenceBlock

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from programs.models import AbstractContentPage
from newamericadotorg.helpers import paginate_results, get_org_wide_posts
from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField

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
        project_root = self.get_parent().specific
        context['project_root'] = project_root
        context['authors'] = project_root.authors.order_by('pk')
        siblings = self.get_siblings(inclusive=True).live().type(InDepthSection)
        siblings_json = json.dumps(SectionSerializer(siblings, many=True).data)
        index = 0
        for i, item in enumerate(siblings):
            if item.id == self.id:
                index = i

        context['index'] = index
        context['siblings'] = siblings
        context['siblings_json'] = siblings_json
        if (index != 0 and len(siblings) > 1):
            context['previous_sibling'] = siblings[(index - 1)]
        if (index != len(siblings) - 1 and len(siblings) > 1):
            context['next_sibling'] = siblings[(index + 1)]

        return context

    class Meta:
        verbose_name = "In-Depth Report Section"

class SectionSerializer(ModelSerializer):
    class Meta:
        model = InDepthSection
        fields = ('id', 'title', 'subheading', 'slug', 'url')

class InDepthProject(Post):
    """

    """
    parent_page_types = ['AllInDepthHomePage']
    subpage_types = ['InDepthSection', 'InDepthProfile']

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

    def get_context(self, request):
        context = super(InDepthProject, self).get_context(request)

        context['project_sections'] = self.get_children().live().type(InDepthSection)
        context['project_root'] = self
        return context

    class Meta:
        verbose_name = "In-Depth Report"


class AllInDepthHomePage(AbstractContentPage):
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
    @property
    def content_model(self):
        return InDepthProject

    class Meta:
        verbose_name = "In-Depth Reports Homepage"

class InDepthProfile(Page):
    parent_page_types = ['InDepthProject']
    subpage_types = []

    subheading = RichTextField(blank=True, null=True)

    datasheet_name = models.CharField(null=False, max_length=150, help_text="The name of the data sheet where the lookup field and query value will be found.")

    lookup_field = models.CharField(null=False, max_length=150, help_text="The name of the field where the query value will be found")

    image_field = models.CharField(max_length=150, blank=True, null=True, help_text="The name of the field where the an image for each profile will be found")

    body = StreamField([
        ('introduction', blocks.RichTextBlock()),
        ('heading', blocks.CharBlock(classname='full title')),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock(icon='image')),
        ('video', EmbedBlock(icon='media')),
        ('table', TableBlock()),
        ('button', ButtonBlock()),
        ('iframe', IframeBlock()),
        ('collapsible', CollapsibleBlock()),
        ('data_reference', DataReferenceBlock()),
        ('video_data_reference', VideoDataReferenceBlock())
    ])

    content_panels = Page.content_panels + [
        FieldPanel('image_field'),
        FieldPanel('subheading'),
        StreamFieldPanel('body'),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('datasheet_name'),
        FieldPanel('lookup_field'),
    ]

    def get_context(self, request):
        context = super(InDepthProfile, self).get_context(request)
        context["project_root"] = self.get_parent()

        return context

    class Meta:
        verbose_name = "In-Depth Report Profile"
