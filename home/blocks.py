from django.db import models
from django import forms

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.contrib.table_block.blocks import TableBlock


class IntegerBlock(blocks.FieldBlock):
	def __init__(self, required=True, help_text=None, max_value=None, min_value=1, **kwargs):
		self.field = forms.IntegerField(required=required, help_text=help_text, max_value=max_value, min_value=min_value)
		super(IntegerBlock, self).__init__(**kwargs)


class ButtonBlock(blocks.StructBlock):
	button_text = blocks.CharBlock(required=True, max_length=50)
	button_link = blocks.URLBlock(required=True, default="https://www.")
	alignment = blocks.ChoiceBlock(choices=[
		('left-aligned', 'Left'),
		('center-aligned', 'Center')
	])

	class Meta:
		template = './blocks/button.html'
		icon = 'radio-full'
		label = 'Button'

class IframeBlock(blocks.StructBlock):
	source_url = blocks.URLBlock(required=True)
	width = IntegerBlock(max_value=1050, help_text="The maximum possible iframe width is 1050")
	height = IntegerBlock()

	class Meta:
		template = './blocks/iframe.html'
		icon = 'form'
		label = 'Iframe'
		help_text= "Specifiy maximum width and height dimensions for the iframe. On smaller screens, width-to-height ratio will be preserved."

class DatavizBlock(blocks.StructBlock):
	title = blocks.CharBlock(required=False)
	subheading = blocks.RichTextBlock(required=False)
	max_width = IntegerBlock()
	show_download_link = blocks.BooleanBlock(default=False, required=False)
	container_id = blocks.CharBlock(required=True)

	class Meta:
		template = './blocks/dataviz.html'
		icon = 'site'
		label = 'Dataviz'

class CollapsibleBody(blocks.StreamBlock):
	heading = blocks.CharBlock(classname='full title')
	paragraph = blocks.RichTextBlock()
	image = ImageChooserBlock(icon='image')
	video = EmbedBlock(icon='media')
	table = TableBlock()
	button = ButtonBlock()
	iframe = IframeBlock()
	dataviz = DatavizBlock()

class CollapsibleBlock(blocks.StructBlock):
	hidden_by_default = CollapsibleBody()

	class Meta:
		template = './blocks/collapsible.html'
		icon = 'arrow-down'
		label = 'Collapsible'

class DataReferenceBlock(blocks.StructBlock):
	display_type = blocks.ChoiceBlock(choices=[
		('in-text', 'In-Text'),
		('fact-box', 'Fact-Box'),
		('list', 'List'),
	])

	display_fields = blocks.ListBlock(blocks.StructBlock([
		('field_name', blocks.CharBlock(required=True)),
    	('format', blocks.ChoiceBlock(choices=[
    		('date', 'Date'),
    		('list', 'List'),
    		('number', 'Number(with thousands-place comma)'),
    		('percent', 'Percent'),
    		('plain_text', 'Plain-text'),
    		('price', 'Price'),
			('rank', 'Rank'),
    	])),
	]))

	class Meta:
		template = './blocks/datareference.html'
		icon = 'cogs'
		label = 'Data Reference'