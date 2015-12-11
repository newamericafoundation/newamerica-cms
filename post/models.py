from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.blocks import ImageChooserBlock

class Post(Page):
	"""Abstract class for pages."""
	is_abstract = True

	class Meta:
		abstract = True

	author = models.CharField(max_length=255)
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

class ProgramPage(Post):
	"""Program page"""
	pass

class BookPage(Post):
	"""Book page"""
	pass
