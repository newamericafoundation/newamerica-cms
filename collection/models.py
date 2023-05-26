from django.db import models
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
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
                    ('page', blocks.PageChooserBlock(page_type=['programs.Program', 'programs.Subprogram'], required=True)),
                    ('description', blocks.CharBlock(required=False, label='Override description text')),
                ],
                icon='doc-empty',
                label='Program',
            ),
        ),
    ],
    blank=True, use_json_field=True)

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
                        ('description', blocks.CharBlock(required=False)),
                        ('program', blocks.CharBlock(required=False, label='Program (shows below description, with resource type)')),
                        ('resource_type', blocks.CharBlock(required=False, label='Resource type, e.g., "External Link" (shows below description, with Program')),
                        ('image', ImageChooserBlock(icon='image', required=False)),
                        ('image_alt_text', blocks.CharBlock(required=False)),
                    ],
                    icon='link',
                    label='External resource',
                ),
            ),
            (
                'attachment',
                blocks.StructBlock(
                    [
                        ('document', DocumentChooserBlock(required=True)),
                        ('title', blocks.CharBlock(required=False, label='Override document title')),
                        ('description', blocks.CharBlock(required=False)),
                        ('program', blocks.CharBlock(required=False, label='Program (shows below description, with resource type)')),
                        ('resource_type', blocks.CharBlock(required=False, label='Resource type, e.g., "Document" (shows below description, with Program)')),
                        ('image', ImageChooserBlock(icon='image', required=False)),
                        ('image_alt_text', blocks.CharBlock(required=False)),
                    ],
                    icon='doc-full',
                    label='Attachment',
                ),
            ),
        ],
        blank=True, use_json_field=True)

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
    use_json_field=True,
    blank=True)

    publications_description = RichTextField(blank=True)
    publications_list = StreamField([
        (
            'publication',
            blocks.StructBlock(
                [
                    ('page', blocks.PageChooserBlock(page_type='home.Post', required=True)),
                    ('title', blocks.CharBlock(required=False, label='Override title')),
                    ('description', blocks.CharBlock(required=False, label='Override description text')),
                    ('image', ImageChooserBlock(icon='image', required=False, label='Override image')),
                    ('image_alt_text', blocks.CharBlock(required=False)),
                ],
                icon='doc-empty',
                label='Publication',
            ),
        ),
    ],
    use_json_field=True,
    blank=True)

    events_description = RichTextField(blank=True)
    events_list = StreamField([
        (
            'event',
            blocks.StructBlock(
                [
                    ('page', blocks.PageChooserBlock(page_type='event.Event', required=True)),
                    ('title', blocks.CharBlock(required=False, label='Override title')),
                    ('description', blocks.CharBlock(required=False, label='Override description text')),
                    ('image', ImageChooserBlock(icon='image', required=False, label='Override image')),
                    ('image_alt_text', blocks.CharBlock(required=False)),
                ],
                icon='date',
                label='Event',
            ),
        ),
    ],
    use_json_field=True,
    blank=True)

    content_panels = AbstractSimplePage.content_panels + [
        FieldPanel('subheading'),
        MultiFieldPanel([
            FieldPanel('programs_description'),
            FieldPanel('programs_list'),
        ],
        heading = 'Programs',
        classname="collapsible"),
        MultiFieldPanel([
            FieldPanel('resources_description'),
            FieldPanel('resources_list'),
        ],
        heading = 'Resources',
        classname="collapsible"),
        MultiFieldPanel([
            FieldPanel('people_description'),
            FieldPanel('people_list'),
        ],
        heading = 'People',
        classname="collapsible"),
        MultiFieldPanel([
            FieldPanel('publications_description'),
            FieldPanel('publications_list'),
        ],
        heading = 'Publications',
        classname="collapsible"),
        MultiFieldPanel([
            FieldPanel('events_description'),
            FieldPanel('events_list'),
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
