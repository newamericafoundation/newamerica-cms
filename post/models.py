from django.db import models
from django.contrib.auth.models import User
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey
from programs.models import Program


class PostProgramRelationship(models.Model):
    program = models.ForeignKey(Program, related_name="+")
    post = ParentalKey('Post', related_name='programs')

    panels = [
        FieldPanel('program'),
    ]


#Abstract Post class that inherits from Page and provides a model template for other content type models
class Post(Page):
    """Abstract class for pages."""

    date = models.DateField("Post date")
    body = StreamField([
        ('heading', blocks.CharBlock(classname='full title')),
        ('paragraph', blocks.RichTextBlock()),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock()),
    ])

    parent_programs = models.ManyToManyField(Program, through=PostProgramRelationship, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        StreamFieldPanel('body'),
        InlinePanel('programs', label=("Programs")),
    ]

    is_creatable = False




class Book(Post):
    """Book page"""
    pass


class Article(Post):
    pass


class Event(Post):
    pass


class Podcasts(Post):
    pass


class PolicyPaper(Post):
    pass


class About(Post):
    pass
