from __future__ import unicode_literals

from django.db import models
from django.db.models import Q

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from programs.models import Program, Subprogram
from person.models import Person

import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('description',)


class HomePage(Page):
    parent_page_types = ['home.HomePage',]

    TEMPLATE_OPTIONS = (
        ('Four Story Template', 'Four Story Template'),
        ('Three Story Template', 'Three Story Template'),
        ('Two Story Template', 'Two Story Template'),
        ('One Story Template', 'One Story Template'),
    )
    template = models.CharField(choices=TEMPLATE_OPTIONS, max_length=50, blank=True, null=True)

    promote_panels = Page.promote_panels + [
        FieldPanel('template'),
    ]


    def get_template(self, request):
        """Allows choice of four templates for homepage"""
        if self.template == 'Four Story Template':
            return 'home/four_story_template.html'
        elif self.template == 'Three Story Template':
            return 'home/three_story_template.html'
        elif self.template == 'Two Story Template':
            return 'home/two_story_template.html'
        elif self.template == 'One Story Template':
            return 'home/one_story_template.html'


    def get_context(self, request):
        context = super(HomePage, self).get_context(request)

        stories = Post.objects.filter(
            Q(lead_story=True) | Q(featured_story=True)
        )
        
        featured_stories = []
        for story in stories:
            if story.lead_story == True:
                lead_story = story
            if story.featured_story == True:
                featured_stories.append(story)

        context['lead_story'] = lead_story

        context['featured_story_1'] = featured_stories[0]
        context['featured_story_2'] = featured_stories[1]
        context['featured_story_3'] = featured_stories[2]
        
        context['lead_image_file_name'] = context['lead_story'].story_image[0].value.filename
        context['featured_story_1_image_file_name'] = featured_stories[0].story_image[0].value.filename
        context['featured_story_2_image_file_name'] = featured_stories[1].story_image[0].value.filename
        context['featured_story_3_image_file_name'] = featured_stories[2].story_image[0].value.filename
        

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

    lead_story = models.NullBooleanField(help_text='Lead story featured most prominently on the homepage or Program page. Most recent story is the one that will appear.')

    featured_story = models.NullBooleanField(help_text='Feature story to appear after the lead story on the homepage or Program page. Most recent featured stories will appear.')

    story_image = StreamField([
        ('story_image', ImageChooserBlock())
        ], blank=True, null=True, help_text='Image to accompany lead or feature story on the homepage or Program page')

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        StreamFieldPanel('body'),
        InlinePanel('programs', label=("Programs")),
        InlinePanel('subprograms', label=("Subprograms")),
        InlinePanel('authors', label=("Authors")),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('lead_story'),
        FieldPanel('featured_story'),
        StreamFieldPanel('story_image'),

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



