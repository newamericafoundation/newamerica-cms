from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from home.models import Post
from programs.models import AbstractContentPage
from newamericadotorg.blocks import ReportSectionBlock
from .utils.docx_save import generate_docx_streamfields
from .blocks import EndnoteBlock

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, StreamFieldPanel, InlinePanel,
    PageChooserPanel, MultiFieldPanel, TabbedInterface, ObjectList)
from wagtail.wagtailcore.blocks import URLBlock, RichTextBlock
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtail.wagtailsearch import index

from home.models import AbstractHomeContentPage

from report.tasks import generate_pdf

class Report(Post):
    """
    Report class that inherits from the abstract
    Post model and creates pages for Policy Papers.
    """
    parent_page_types = ['ReportsHomepage']
    subpage_types = []

    sections = StreamField([
        ('section', ReportSectionBlock(template="components/report_section_body.html"))
    ])

    acknowledgements = models.TextField(blank=True, null=True)

    source_word_doc = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Source Word Document'
    )

    report_pdf = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Report PDF'
    )

    overwrite_sections_on_save = models.BooleanField(default=False, help_text='If checked, sections and endnote fields will be overwritten with Word document source on save. Use with CAUTION!')
    generate_pdf_on_publish = models.BooleanField(default=False, help_text='If checked, the "Report PDF" field will be filled with a generated pdf. Otherwise, leave this unchecked and upload a pdf to the "Report PDF" field')
    revising = False

    endnotes = StreamField([
        ('endnote', EndnoteBlock()),
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

    content_panels = Post.content_panels + [
        FieldPanel('acknowledgements'),
    ]

    sections_panels = [
        MultiFieldPanel([
            DocumentChooserPanel('source_word_doc'),
            FieldPanel('overwrite_sections_on_save'),
        ]),
        MultiFieldPanel([
            FieldPanel('generate_pdf_on_publish'),
            DocumentChooserPanel('report_pdf'),
            StreamFieldPanel('attachment')
        ]),
        StreamFieldPanel('sections')
    ]

    endnote_panels = [StreamFieldPanel('endnotes')]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="Content"),
        ObjectList(sections_panels, heading="Sections"),
        ObjectList(endnote_panels, heading="Endnotes"),
        ObjectList(Post.promote_panels, heading="Promote"),
        ObjectList(Post.settings_panels, heading='Settings', classname="settings"),
    ])

    search_fields = Post.search_fields + [index.SearchField('sections')]

    def save(self, *args, **kwargs):
        if not self.revising and self.source_word_doc is not None and self.overwrite_sections_on_save:
            self.revising = True
            self.overwrite_sections_on_save = False
            streamfields = generate_docx_streamfields(self.source_word_doc.file)
            self.sections = streamfields['sections']
            self.endnotes = streamfields['endnotes']
            self.revising = False

        if not self.revising and not self.has_unpublished_changes and self.generate_pdf_on_publish:
            self.revising = True # generate_pdf resets this to False
            generate_pdf.apply_async(args=(self.id,))

        super(Report, self).save(*args, **kwargs)



    class Meta:
        verbose_name = 'Report'


class AllReportsHomePage(AbstractHomeContentPage):
    """
    A page which inherits from the abstract Page model and
    returns every Report in the Report model
    for the organization wide Report omepage
    """
    parent_page_types = ['home.Homepage']
    subpage_types = []

    @property
    def content_model(self):
        return Report

    class Meta:
        verbose_name = "Reports Homepage"


class ReportsHomepage(AbstractContentPage):
    """
    A page which inherits from the abstract Page model and
    returns all Reports associated with a specific
    Program or Subprogram
    """
    parent_page_types = ['programs.Program', 'programs.Subprogram']
    subpage_types = ['Report']

    @property
    def content_model(self):
        return Report

    class Meta:
        verbose_name = "Reports Homepage"
