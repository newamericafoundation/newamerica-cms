import json

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

from home.models import Post
from programs.models import AbstractContentPage
from .blocks import EndnoteBlock, ReportSectionBlock, FeaturedReportSectionBlock

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page, PageRevision
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel, StreamFieldPanel, InlinePanel,
    PageChooserPanel, MultiFieldPanel, TabbedInterface, ObjectList)
from wagtail.core.blocks import URLBlock, RichTextBlock
from wagtail.core.fields import RichTextField
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.search import index

from home.models import AbstractHomeContentPage

from .tasks import generate_pdf, parse_pdf, write_pdf, generate_report_contents, get_report_authors


class Report(RoutablePageMixin, Post):
    """
    Report class that inherits from the abstract
    Post model and creates pages for Policy Papers.
    """
    parent_page_types = ['ReportsHomepage']
    subpage_types = []

    sections = StreamField([
        ('section', ReportSectionBlock(template="components/report_section_body.html", required=False))
    ], null=True, blank=True)

    abstract = RichTextField(blank=True, null=True)

    acknowledgements = RichTextField(blank=True, null=True)

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

    dataviz_src = models.CharField(blank=True, null=True, max_length=300, help_text="")

    overwrite_sections_on_save = models.BooleanField(default=False, help_text='If checked, sections and endnote fields ⚠ will be overwritten ⚠ with Word document source on save. Use with CAUTION!')
    generate_pdf_on_publish = models.BooleanField('Generate PDF on save', default=False, help_text='⚠ Save latest content before checking this ⚠\nIf checked, the "Report PDF" field will be filled with a generated pdf. Otherwise, leave this unchecked and upload a pdf to the "Report PDF" field.')
    revising = False

    featured_sections = StreamField([
        ('featured', FeaturedReportSectionBlock(required=False, null=True)),
    ], null=True, blank=True)

    endnotes = StreamField([
        ('endnote', EndnoteBlock(required=False, null=True)),
    ], null=True, blank=True)

    report_url = StreamField([
        ('report_url', URLBlock(required=False, null=True)),
    ], null=True, blank=True)

    attachment = StreamField([
        ('attachment', DocumentChooserBlock(required=False, null=True)),
    ], null=True, blank=True)

    partner_logo = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('subheading'),
            FieldPanel('date'),
            ImageChooserPanel('story_image'),
        ]),
        InlinePanel('authors', label=("Authors")),
        InlinePanel('programs', label=("Programs")),
        InlinePanel('subprograms', label=("Subprograms")),
        InlinePanel('topics', label=("Topics")),
        InlinePanel('location', label=("Locations")),
        MultiFieldPanel([
            FieldPanel('abstract'),
            StreamFieldPanel('featured_sections'),
            FieldPanel('acknowledgements'),
        ])
    ]

    sections_panels = [
        StreamFieldPanel('sections')
    ]

    endnote_panels = [StreamFieldPanel('endnotes')]

    settings_panels = Post.settings_panels + [FieldPanel('dataviz_src')]

    promote_panels = Page.promote_panels + [
        FieldPanel('story_excerpt'),
    ]

    pdf_panels = [
        MultiFieldPanel([
            DocumentChooserPanel('source_word_doc'),
            FieldPanel('overwrite_sections_on_save'),
        ], heading='Word Doc Import'),
        MultiFieldPanel([
            FieldPanel('generate_pdf_on_publish'),
            DocumentChooserPanel('report_pdf'),
            StreamFieldPanel('attachment')
        ], heading='PDF Generation'),
        ImageChooserPanel('partner_logo')
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="Landing"),
        ObjectList(sections_panels, heading="Sections"),
        ObjectList(endnote_panels, heading="Endnotes"),
        ObjectList(promote_panels, heading="Promote"),
        ObjectList(settings_panels, heading='Settings', classname="settings"),
        ObjectList(pdf_panels, heading="PDF Publishing")
    ])

    search_fields = Post.search_fields + [index.SearchField('sections')]

    def get_context(self, request):
        context = super().get_context(request)

        if getattr(request, 'is_preview', False):
            import newamericadotorg.api.report
            revision = PageRevision.objects.filter(page=self).last().as_page_object()
            report_data = newamericadotorg.api.report.serializers.ReportDetailSerializer(revision).data
            context['initial_state'] = json.dumps(report_data)

        return context

    def save(self, *args, **kwargs):
        super(Report, self).save(*args, **kwargs)

        if not self.overwrite_sections_on_save and not self.generate_pdf_on_publish:
            self.revising = False

        if not self.revising and self.source_word_doc is not None and self.overwrite_sections_on_save:
            self.revising = True
            parse_pdf(self)
            self.overwrite_sections_on_save = False
            self.save_revision()

        if not self.revising and self.generate_pdf_on_publish:
            generate_pdf.apply_async(args=(self.id,))

    # Extra views

    @route(r'pdf/$')
    def pdf(self, request):
        if not self.report_pdf:
            return self.pdf_render(request)
        url = 'https://s3.amazonaws.com/newamericadotorg/' + self.report_pdf.file.name
        return redirect(url)

    @route(r'pdf/render/$')
    def pdf_render(self, request):
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; filename=%s.pdf' % self.title
        response['Content-Transfer-Encoding'] = 'binary'
        protocol = 'https://' if request.is_secure() else 'http://'
        base_url = protocol + request.get_host()

        contents = generate_report_contents(self)
        authors = get_report_authors(self)

        html = loader.get_template('report/pdf.html').render({
            'page': self,
            'contents': contents,
            'authors': authors
        })
        pdf = write_pdf(response, html, base_url)

        return response

    @route(r'print/$')
    def print(self, request):
        contents = generate_report_contents(self)
        authors = get_report_authors(self)

        return render(request, 'report/pdf.html', context={ 'page': self, 'contents': contents, 'authors': authors })

    @route(r'[a-zA-Z0-9_\.\-]*/$')
    def section(self, request):
        # Serve the whole report, subsection routing is handled by React
        return self.serve(request)

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
    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = ['Report']

    @property
    def content_model(self):
        return Report

    class Meta:
        verbose_name = "Reports Homepage"
