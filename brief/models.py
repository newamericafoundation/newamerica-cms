from django.core.exceptions import ValidationError
from django.db import models
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.documents.blocks import DocumentChooserBlock

from home.models import AbstractHomeContentPage, Post
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

    def word_count(self):
        countable_block_types = {'paragraph', 'introduction', 'heading'}
        count = 0
        for block in self.body:
            if block.block_type in countable_block_types:
                text = getattr(block.value, 'source', block.value)
                count += len(str(text).split())
        return count

    def clean(self):
        super().clean()

        word_limit = 3000
        word_count = self.word_count()
        if word_count > word_limit:
            raise ValidationError(
                f'Body of brief cannot exceed {word_limit} words across introductions, headings, and paragraphs. Currently used: {word_count} words.'
            )


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
