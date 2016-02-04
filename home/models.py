from __future__ import unicode_literals

from django.db import models
from django.db.models import Q

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey
from programs.models import Program, Subprogram
from person.models import Person

import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('description',)


class HomePage(Page):
    parent_page_types = ['home.HomePage',]

    TEMPLATE_OPTIONS = (
        (4, 'Four Story Template'),
        (3, 'Three Story Template'),
        (2, 'Two Story Template'),
        (1, 'One Story Template'),
    )
    template = models.IntegerField(choices=TEMPLATE_OPTIONS, default=3)

    promote_panels = Page.promote_panels + [
        FieldPanel('template'),
    ]

    def get_template(self, request):
        """Allows choice of four templates for homepage"""
        if self.template == 4:
            return 'home/four_story_template.html'
        elif self.template == 3:
            return 'home/three_story_template.html'
        elif self.template == 2:
            return 'home/two_story_template.html'
        elif self.template == 1:
            return 'home/one_story_template.html'


    def get_context(self, request):
        context = super(HomePage, self).get_context(request)

        context['lead_story'] = Post.objects.filter(home_page_status=1) \
            .order_by('-date').first()

        number_of_featured_stories = self.template-1
        if number_of_featured_stories > 1:
            context['featured_stories'] = Post.objects.filter(home_page_status=2) \
                .order_by('-date')[:number_of_featured_stories]
        
        return context


class SimplePage(Page):
    """
    Simple page class that inherits from the Page model and
    creates simple, generic pages.
    """
    subpage_types = ['SimplePage']
    body = StreamField([
        ('heading', blocks.CharBlock(classname='full title')),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock(icon='image')),
        ('video', EmbedBlock(icon='media')),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]

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

    STORY_TYPE = (
        (0, 'Regular Story'),
        (1, 'Lead Story'),
        (2, 'Feature Story'),
    )
    program_page_status = models.IntegerField(choices=STORY_TYPE, default=0)
    home_page_status = models.IntegerField(choices=STORY_TYPE, default=0)

    story_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        StreamFieldPanel('body'),
        InlinePanel('programs', label=("Programs")),
        InlinePanel('subprograms', label=("Subprograms")),
        InlinePanel('authors', label=("Authors")),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('program_page_status'),
        FieldPanel('home_page_status'),
        ImageChooserPanel('story_image'),

    ]

    is_creatable = False

    def save(self, *args, **kwargs):
        """
        This save method overloads the wagtailcore Page save method in
        order to ensure that the parent program - post relationship is
        captured even if the user does not select it.
        """
        super(Post, self).save(*args, **kwargs)
        parent_program_page = self.get_parent().get_parent()
        parent_program = Program.objects.get(
            slug=parent_program_page.slug
        )
        relationship, created = PostProgramRelationship.objects.get_or_create(
            program=parent_program, post=self
        )
        if created:
            relationship.save()



