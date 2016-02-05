from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtaildocs.blocks import DocumentChooserBlock

from wagtail.wagtaildocs.models import Document
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel,MultiFieldPanel, \
    InlinePanel, PageChooserPanel, StreamFieldPanel


class MapBlock(blocks.StructBlock):
    data_file = DocumentChooserBlock()
    doc_uploaded = blocks.BooleanBlock(required=True)
    variable_option = blocks.CharBlock(required=True,max_length=500)
 
    class Meta:
        template = './home/map.html'
        icon = 'cogs'
        label = 'Map'