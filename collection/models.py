from django.db import models
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from home.models import AbstractSimplePage
from programs.models import AbstractContentPage

class Collection(AbstractSimplePage):
    parent_page_types = ['CollectionsHomePage']
    subpage_types = []

    subheading = models.TextField(blank=True, null=True)

    programs_description = RichTextField(blank=True)
    programs_list = StreamField([
        (
            'program',
            blocks.StructBlock(
                [
                    ('page', blocks.PageChooserBlock(page_type='programs.Program', required=True)),
                    ('description', blocks.RichTextBlock(required=False)),
                ],
                icon='doc-empty',
                label='Program',
            ),
        ),
    ],
    blank=True)

    # TODO: resources properly
    resources_description = RichTextField(blank=True)
    resources_list = StreamField(
        [
            (
                'external_resource',
                blocks.StructBlock(
                    [
                        ('link', blocks.URLBlock(required=True)),
                        ('title', blocks.CharBlock(required=True)),
                        ('description', blocks.RichTextBlock(required=False)),
                        ('image', ImageChooserBlock(icon='image', required=False)),
                    ],
                    icon='link-external',
                    label='External resource',
                ),
            ),
            (
                'attachment',
                blocks.StructBlock(
                    [
                        ('document', DocumentChooserBlock(required=True)),
                        ('title', blocks.CharBlock(required=True)),
                        ('description', blocks.RichTextBlock(required=False)),
                        ('image', ImageChooserBlock(icon='image', required=False)),
                    ],
                    icon='doc-full',
                    label='Attachment',
                ),
            ),
        ],
    blank=True)

    people_description = RichTextField(blank=True)
    people_list = StreamField([
        (
            'person', blocks.PageChooserBlock(
                page_type='person.Person',
                icon='user',
                label='Person',
            )
        ),
    ],
    blank=True)

    publications_description = RichTextField(blank=True)
    publications_list = StreamField([
        (
            'publication',
            blocks.StructBlock(
                [
                    ('page', blocks.PageChooserBlock(page_type='home.Post', required=True)),
                    ('title', blocks.CharBlock(required=False)),
                    ('description', blocks.RichTextBlock(required=False)),
                    ('image', ImageChooserBlock(icon='image', required=False)),
                ],
                icon='doc-empty',
                label='Publication',
            ),
        ),
    ],
    blank=True)

    events_description = RichTextField(blank=True)
    events_list = StreamField([
        (
            'event',
            blocks.StructBlock(
                [
                    ('page', blocks.PageChooserBlock(page_type='event.Event', required=True)),
                    ('title', blocks.CharBlock(required=False)),
                    ('image', ImageChooserBlock(icon='image', required=False)),
                    ('description', blocks.RichTextBlock(required=False)),
                ],
                icon='date',
                label='Event',
            ),
        ),
    ],
    blank=True)

    content_panels = AbstractSimplePage.content_panels + [
        FieldPanel('subheading'),
        MultiFieldPanel([
            FieldPanel('programs_description'),
            StreamFieldPanel('programs_list'),
        ],
        heading = 'Programs',
        classname="collapsible"),
        MultiFieldPanel([
            FieldPanel('resources_description'),
            StreamFieldPanel('resources_list'),
        ],
        heading = 'Resources',
        classname="collapsible"),
        MultiFieldPanel([
            FieldPanel('people_description'),
            StreamFieldPanel('people_list'),
        ],
        heading = 'People',
        classname="collapsible"),
        MultiFieldPanel([
            FieldPanel('publications_description'),
            StreamFieldPanel('publications_list'),
        ],
        heading = 'Publications',
        classname="collapsible"),
        MultiFieldPanel([
            FieldPanel('events_description'),
            StreamFieldPanel('events_list'),
        ],
        heading = 'Events',
        classname="collapsible"),
    ]

    class Meta:
        verbose_name = 'Collection'

class CollectionsHomePage(AbstractContentPage):
    parent_page_types = ['home.HomePage']
    subpage_types = ['Collection']

    class Meta:
        verbose_name = "Collections Homepage"
