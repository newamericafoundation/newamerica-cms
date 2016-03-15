from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.blocks import PageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, StreamFieldPanel, InlinePanel,
    PageChooserPanel, MultiFieldPanel)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey
from programs.models import AbstractProgram, Program, Subprogram
from person.models import Person

import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('description',)


class HomePage(Page):
    parent_page_types = ['home.HomePage', ]

    # Up to four lead stories can be featured on the homepage.
    # Lead_1 will be featured most prominently.
    lead_1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    lead_2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    lead_3 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    lead_4 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    # Up to three featured stories to appear underneath
    # the lead stories. All of the same size and formatting.
    feature_1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    feature_2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    feature_3 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    featured_stories = [feature_1, feature_2, feature_3]

    #Up to three recent items that are below the
    #featured stories banner that circle through a carousel
    recent_carousel = StreamField([
        ('event', PageChooserBlock()),
        ('policy_paper', PageChooserBlock()),
    ], blank=True)


    promote_panels = Page.promote_panels + [
        MultiFieldPanel(
            [
                PageChooserPanel('lead_1'),
                PageChooserPanel('lead_2'),
                PageChooserPanel('lead_3'),
                PageChooserPanel('lead_4'),
            ],
            heading="Lead Stories",
            classname="collapsible"
        ),
        MultiFieldPanel(
            [
                PageChooserPanel('feature_1'),
                PageChooserPanel('feature_2'),
                PageChooserPanel('feature_3'),
            ],
            heading="Featured Stories",
            classname="collapsible"
        ),
        StreamFieldPanel('recent_carousel'),
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)

        context['other_lead_stories'] = []

        if self.lead_2:
            context['other_lead_stories'].append(self.lead_2)
        if self.lead_3:
            context['other_lead_stories'].append(self.lead_3)
        if self.lead_4:
            context['other_lead_stories'].append(self.lead_4)

        context['featured_stories'] = [
            self.feature_1, self.feature_2, self.feature_3
        ]

        return context



class AbstractSimplePage(Page):
    """
    Abstract Simple page class that inherits from the Page model and
    creates simple, generic pages.
    """
    body = StreamField([
        ('heading', blocks.CharBlock(classname='full title')),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock(icon='image')),
        ('video', EmbedBlock(icon='media')),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]

    class Meta:
        abstract = True


class OrgSimplePage(AbstractSimplePage):
    """
    Simple Page at the organization level
    """
    parent_page_types = ['home.HomePage', 'OrgSimplePage']
    subpage_types = ['OrgSimplePage']



class ProgramSimplePage(AbstractSimplePage):
    """
    Simple Page at the Program level
    """
    parent_page_types = ['programs.Program', 'ProgramSimplePage']
    subpage_types = ['ProgramSimplePage']



class PostAuthorRelationship(models.Model):
    """
    Through model that maps the many to many
    relationship between Post and Authors
    """
    author = models.ForeignKey(Person, related_name="+")
    post = ParentalKey('Post', related_name='authors')

    panels = [
        FieldPanel('author'),
    ]


class PostProgramRelationship(models.Model):
    """
    Through model that maps the many to many
    relationship between Post and Programs
    """

    program = models.ForeignKey(Program, related_name="+")
    post = ParentalKey('Post', related_name='programs')

    panels = [
        FieldPanel('program'),
    ]

    class meta:
        unique_together = (("program", "post"),)

    def __str__(self):
        return str(self.program) + "," + str(self.post)


class PostSubprogramRelationship(models.Model):
    """
    Through model that maps the many to many
    relationship between Post and Subprograms
    """

    subprogram = models.ForeignKey(Subprogram, related_name="+")
    post = ParentalKey('Post', related_name='subprograms')

    panels = [
        FieldPanel('subprogram'),
    ]
    class meta:
        unique_together = (("subprogram", "post"),)


class Post(Page):
    """
    Abstract Post class that inherits from Page
    and provides a model template for other content
    type models
    """

    date = models.DateField("Post date")

    headline = models.TextField(default='No Heading Provided')
    sub_headline = models.TextField(blank=True, null=True)

    body = StreamField([
        ('heading', blocks.CharBlock(classname='full title')),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock(icon='image')),
        ('video', EmbedBlock(icon='media')),
    ])

    parent_programs = models.ManyToManyField(
        Program, through=PostProgramRelationship, blank=True)

    post_subprogram = models.ManyToManyField(
        Subprogram, through=PostSubprogramRelationship, blank=True)

    post_author = models.ManyToManyField(
        Person, through=PostAuthorRelationship, blank=True)

    story_excerpt = models.CharField(blank=True, max_length=140)

    story_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('headline'),
        FieldPanel('sub_headline'),
        StreamFieldPanel('body'),
        InlinePanel('programs', label=("Programs")),
        InlinePanel('subprograms', label=("Subprograms")),
        InlinePanel('authors', label=("Authors")),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('story_excerpt'),
        ImageChooserPanel('story_image'),
    ]

    is_creatable = False

    def get_context(self, request):
        context = super(Post, self).get_context(request)
        context['authors'] = self.authors.order_by('pk')

        return context

    def save(self, *args, **kwargs):
        """
        This save method overloads the wagtailcore Page save method in
        order to ensure that the parent program - post relationship is
        captured even if the user does not select it.
        """
        super(Post, self).save(*args, **kwargs)
        parent_page = self.get_parent().get_parent()
        parent_program = Program.objects.get(
            slug=parent_page.slug
        )
        if isinstance(parent_program, AbstractProgram):
            relationship, created=PostProgramRelationship.objects.get_or_create(
                program=parent_program, post=self
            )
            if created:
                relationship.save()
