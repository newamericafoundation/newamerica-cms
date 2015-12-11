from django.db import models
from django.contrib.auth.models import User
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey


class Post(Page):
	"""Abstract class for pages."""
	is_abstract = True

	class Meta:
		abstract = True

	author = models.ForeignKey(User)
	date = models.DateField("Post date")
	body = StreamField([
        ('heading', blocks.CharBlock(classname='full title')),
        ('paragraph', blocks.RichTextBlock()),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock()),
    ])

	content_panels = Page.content_panels + [
		FieldPanel('author'), 
		FieldPanel('date'), 
		StreamFieldPanel('body'),
	]

class Program(Post):
	"""Program model"""


class Subprogram(Post):
	"""Subprogram model"""


class ProgramRelationship():
	subprogram = models.ForeignKey(Subprogram, related_name="+")
	program = ParentalKey('Program', related_name='subprogram')
	panels = [
		Field
	]


class Book(Post):
	"""Book page"""
	pass

https://github.com/torchbox/wagtail/issues/231
