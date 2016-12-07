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
    title = blocks.TextBlock(required=False)
    description = blocks.RichTextBlock()
    image = ImageChooserBlock(icon='image', required=False)
    twitter = blocks.URLBlock(required=False)

class PeopleBlock(blocks.StreamBlock):
    person = PersonBlock();

    class Meta:
        template = 'blocks/people.html'

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
        ('lecture', 'Lecture'),
        ('break', 'Break'),
        ('meal', 'Meal'),
        ('reception','Reception'),
        ('registration', 'Registration')
    )

class SessionSpeakerBlock(blocks.StructBlock):
    name = blocks.TextBlock(required=True)
    title = blocks.TextBlock(required=False)

class SessionBlock(blocks.StructBlock):
    name = blocks.TextBlock()
    session_type = SessionTypesBlock()
    description = blocks.RichTextBlock(required=False)
    start_time = blocks.TimeBlock(required=False)
    end_time = blocks.TimeBlock(required=False)
    speakers = blocks.StreamBlock([
        ('speaker', SessionSpeakerBlock())
    ])
    archived_video_link = blocks.URLBlock(help_text="Enter youtube link after conference", required=False)

class SessionDayBlock(blocks.StructBlock):
    day = IntegerChoiceBlock(help_text="What day of the conference is this session on?", required=False)
    start_time = blocks.TimeBlock(required=False)
    end_time = blocks.TimeBlock(required=False)
    sessions = blocks.StreamBlock([
        ('session', SessionBlock())
    ])

class SessionsBlock(blocks.StreamBlock):
    days = SessionDayBlock()

    class Meta:
        template = 'blocks/schedule.html'

class PartnerTypeBlock(blocks.ChoiceBlock):
    choices = (
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

class TwoColumnBlock(blocks.StructBlock):
    left_column = blocks.RichTextBlock()
    right_column = blocks.RichTextBlock()

    class Meta:
        template = 'blocks/two-column.html'

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
