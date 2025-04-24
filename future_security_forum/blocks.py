from django.db import models
from django import forms

from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
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
    logo_alt_text = blocks.CharBlock(
        required=False,
        verbose_name='Logo alternative text',
        help_text='A concise description of the image for users of assistive technology.',
    )

class PartnersBlock(blocks.StreamBlock):
    partner = PartnerBlock()

    class Meta:
        template = 'fsf-blocks/partners.html'
        required=False

class DirectionBlock(blocks.StructBlock):
    transportation_type = blocks.CharBlock(help_text="e.g car, metro, taxi")
    directions = blocks.RichTextBlock()

class DirectionsBlock(blocks.StreamBlock):
    direction = DirectionBlock()

    class Meta:
        template = 'fsf-blocks/directions.html'

class VenueBlock(blocks.StreamBlock):
    paragraph = blocks.RichTextBlock()
    columns = TwoColumnBlock()
from django.db import models
from django import forms

from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
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
    logo_alt_text = blocks.CharBlock(
        required=False,
        verbose_name='Logo alternative text',
        help_text='A concise description of the image for users of assistive technology.',
    )

class PartnersBlock(blocks.StreamBlock):
    partner = PartnerBlock()

    class Meta:
        template = 'blocks/partners.html'
        required=False

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
