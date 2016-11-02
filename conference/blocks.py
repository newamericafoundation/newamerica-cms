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


class PersonBlock(blocks.StructBlock):
    name = blocks.TextBlock(required=True)
    title = blocks.TextBlock()
    description = blocks.RichTextBlock()
    image = ImageChooserBlock(icon='image')
    twitter = blocks.URLBlock()

class PeopleBlock(blocks.StreamBlock):
    person = PersonBlock();

class IntegerChoiceBlock(blocks.ChoiceBlock):
    choices = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5','5'),
        ('6', '6')
    )

class SessionTypesBlock(blocks.ChoiceBlock):
    choices = (
        ('panel', 'Panel'),
        ('speaker', 'Speaker'),
        ('break', 'Break'),
        ('meal', 'Meal'),
        ('reception','Reception'),
        ('registration', 'Registration')
    )

class SessionSpeakerBlock(blocks.StructBlock):
    name = blocks.TextBlock(required=True)
    title = blocks.TextBlock()

class SessionBlock(blocks.StructBlock):
    day = IntegerChoiceBlock(help_text="What day of the conference is this session on?")
    name = blocks.TextBlock()
    session_type = SessionTypesBlock()
    description = blocks.RichTextBlock()
    start_time = blocks.TimeBlock()
    end_time = blocks.TimeBlock()
    speakers = blocks.StreamBlock([
        ('speaker', SessionSpeakerBlock())
    ])
    archived_video_link = blocks.URLBlock(help_text="Enter youtube link after conference")

class SessionsBlock(blocks.StreamBlock):
    session = SessionBlock()

class PartnerTypeBlock(blocks.ChoiceBlock):
    choices = (
        ('premier_sponsor', 'Premier Sponsor'),
        ('sponsor', 'Sponsor'),
        ('media_partner', 'Media Partner'),
        ('recognized_partner', 'Recognized Partner')
    )

class PartnerBlock(blocks.StructBlock):
    name = blocks.TextBlock()
    logo = ImageChooserBlock(icon='image')
    type = PartnerTypeBlock()

class PartnersBlock(blocks.StreamBlock):
    partner = PartnerBlock()

class TwoColumnBlock(blocks.StructBlock):
    left_column = blocks.RichTextBlock()
    right_column = blocks.RichTextBlock()

class DirectionBlock(blocks.StructBlock):
    transportation_type = blocks.CharBlock(help_text="e.g car, metro, taxi")
    directions = blocks.RichTextBlock()

class DirectionsBlock(blocks.StreamBlock):
    direction = DirectionBlock()

class VenueBlock(blocks.StreamBlock):
    paragraph = blocks.RichTextBlock()
    columns = TwoColumnBlock()
