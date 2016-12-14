from django.db import models
from django import forms

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore import blocks
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.contrib.table_block.blocks import TableBlock
from home.blocks import IntegerBlock

class GoogleMapBlock(blocks.StructBlock):
    use_page_address = blocks.BooleanBlock(default=False, required=False, help_text="If selected, map will use the address already defined for this page.")
    street = blocks.TextBlock(required=False)
    city = blocks.TextBlock(required=False, default='Washington')
    state = blocks.TextBlock(required=False, default='D.C.')
    zipcode = blocks.TextBlock(required=False, default='200')

    class Meta:
        template = 'blocks/google_map.html'
