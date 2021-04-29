from django.core.exceptions import ValidationError
from django.db import models
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.documents.blocks import DocumentChooserBlock

from home.models import AbstractHomeContentPage, Post
from programs.models import AbstractContentPage


def word_count_body_block(body_block):
    countable_block_types = {'paragraph', 'introduction', 'heading'}
    count = 0
    for block in body_block:
        if block.block_type in countable_block_types:
            text = getattr(block.value, 'source', block.value)
            count += len(str(text).split())
        elif block.block_type == 'resource_kit':
            count += len(block.value.get('title', '').split())
            count += len(block.value.get('description', '').split())
            for block_type, data, _ in block.value['resources'].stream_data:
                count += len(data.get('name', '').split())
                if data.get('description', False):
                    count += len(str(data['description'].source).split())
        elif block.block_type == 'panels':
            for block_type, data, _ in block.value.stream_data:
                count += len(data.get('title', '').split())
                if data.get('body'):
                    count += word_count_body_block(data['body'])
    return count


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
        return word_count_body_block(self.body)

    def clean(self):
        super().clean()

        word_limit = 3000
        word_count = self.word_count()
        if word_count > word_limit:
            raise ValidationError(
                f'Body of brief cannot exceed {word_limit} words across introductions, headings, and paragraphs. Currently used: {word_count} words.'
            )

    class Meta:
        verbose_name = 'Briefs Homepage'

class ProgramBriefsPage(AbstractContentPage):
    """
    A page which inherits from the abstract Page model and
    returns all Briefs associated with a specific
    Program or Subprogram
    """
    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = ['Brief']

    @property
    def content_model(self):
        return Brief

    class Meta:
        verbose_name = 'Briefs Homepage'


class AllBriefsHomePage(AbstractHomeContentPage):
    """
    A page which inherits from the abstract Page model and
    returns every Brief in the Brief model
    for the organization wide Brief Homepage
    """
    parent_page_types = ['home.Homepage']
    subpage_types = []

    @property
    def content_model(self):
        return Brief

    class Meta:
        verbose_name = 'Homepage for all Briefs'
