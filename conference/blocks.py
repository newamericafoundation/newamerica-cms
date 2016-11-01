from django.db import models
from django import forms

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.contrib.table_block.blocks import TableBlock
from home.blocks import IntegerBlock


class SpeakerBlock(blocks.StructBlock):
    name = blocks.TextBlock(required=True)
    title = blocks.TextBlock()
    description = blocks.RichTextBlock()
    image = ImageChooserBlock(icon='image')
    twitter = blocks.URLBlock()

class SessionSpeakerBlock(blocks.StructBlock):
    name = blocks.TextBlock(required=True)
    title = blocks.TextBlock()
