from django.db import models
from django import forms

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock
from newamericadotorg.blocks import IntegerBlock, TwoColumnBlock

class PartnerTypeBlock(blocks.ChoiceBlock):
    choices = (
        ('no_type', 'None'),
        ('premier_sponsor', 'Premier Sponsor'),
        ('sponsor', 'Sponsor'),
        ('media_partner', 'Media Partner'),
        ('recognized_partner', 'Recognized Partner')
    )

class PartnerBlock(blocks.StructBlock):
    name = blocks.TextBlock()
    type = PartnerTypeBlock()
    logo = ImageChooserBlock(icon='image', required=False)

class PartnersBlock(blocks.StreamBlock):
    partner = PartnerBlock()

    class Meta:
        template = 'blocks/partners.html'

class DirectionBlock(blocks.StructBlock):
    transportation_type = blocks.CharBlock(help_text="e.g car, metro, taxi")
    directions = blocks.RichTextBlock()

class DirectionsBlock(blocks.StreamBlock):
    direction = DirectionBlock()

    class Meta:
        template = 'blocks/directions.html'

class VenueBlock(blocks.StreamBlock):
    paragraph = blocks.RichTextBlock()
    columns = TwoColumnBlock()
