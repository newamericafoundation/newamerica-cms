from django.db import models
from django import forms

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore import blocks
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.contrib.table_block.blocks import TableBlock
from mysite.blocks import IntegerBlock, TwoColumnBlock

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
