from django.db import models

from home.models import Post
from programs.models import AbstractContentPage
from newamericadotorg.blocks import PanelBlock

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, StreamFieldPanel, InlinePanel,
    PageChooserPanel, MultiFieldPanel, TabbedInterface, ObjectList)
from wagtail.wagtailcore.blocks import URLBlock, RichTextBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtail.wagtailsearch import index

class Report(Post):
    """
    Report class that inherits from the abstract
    Post model and creates pages for Policy Papers.
    """
    parent_page_types = ['ReportsHomepage']
    subpage_types = []

    sections = StreamField([
        ('section', PanelBlock()),
    ])

    endnotes = StreamField([
        ('endnote', RichTextBlock()),
    ])

    report_url = StreamField([
        ('report_url', URLBlock(required=False, null=True)),
    ])

    attachment = StreamField([
        ('attachment', DocumentChooserBlock(required=False, null=True)),
    ])

    publication_cover_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = Page.content_panels + [
        FieldPanel('subheading'),
        FieldPanel('date'),
        InlinePanel('programs', label=("Programs")),
        InlinePanel('subprograms', label=("Subprograms")),
        InlinePanel('authors', label=("Authors")),
        InlinePanel('topics', label=("Topics")),
        StreamFieldPanel('report_url'),
        StreamFieldPanel('attachment'),
        ImageChooserPanel('publication_cover_image'),
    ]

    sections_panels = [StreamFieldPanel('sections')]

    endnote_panels = [StreamFieldPanel('endnotes')]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="Content"),
        ObjectList(sections_panels, heading="Sections"),
        ObjectList(endnote_panels, heading="Endnotes"),
        ObjectList(Post.promote_panels, heading="Promote"),
        ObjectList(Post.settings_panels, heading='Settings', classname="settings"),
    ])

    search_fields = Post.search_fields + [index.SearchField('sections')]

    class Meta:
        verbose_name = 'Report'

class AllReportsHomePage(Page):
    """
    A page which inherits from the abstract Page model and
    returns every Report in the Report model
    for the organization wide Report omepage
    """
    parent_page_types = ['home.Homepage']
    subpage_types = []

    class Meta:
        verbose_name = "Organization-wide Reports Homepage"


class ReportsHomepage(AbstractContentPage):
    """
    A page which inherits from the abstract Page model and
    returns all Reports associated with a specific
    Program or Subprogram
    """
    parent_page_types = ['programs.Program', 'programs.Subprogram']
    subpage_types = ['Report']


    class Meta:
        verbose_name = "Reports Homepage"
