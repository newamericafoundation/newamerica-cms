from django.db import models
from wagtail.core.fields import StreamField
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.admin.edit_handlers import StreamFieldPanel

from home.models import Post, AbstractHomeContentPage
from programs.models import AbstractContentPage


class Brief(Post):
    parent_page_types = ['ProgramBriefsPage']
    subpage_types = []

    attachment = StreamField(
        [
            ('attachment', DocumentChooserBlock(required=False, null=True)),
        ],
        null=True,
        blank=True,
    )

    content_panels = Post.content_panels + [
        StreamFieldPanel('attachment'),
    ]


class ProgramBriefsPage(AbstractContentPage):
    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = ['Brief']

    @property
    def content_model(self):
        return Brief

    class Meta:
        verbose_name = 'Briefs Homepage'


class AllBriefsHomePage(AbstractHomeContentPage):
    parent_page_types = ['home.Homepage']
    subpage_types = []

    @property
    def content_model(self):
        return Brief

    class Meta:
        verbose_name = 'Homepage for all briefs'
