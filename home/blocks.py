from django.db import models
from django import forms

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.wagtailcore.blocks import IntegerBlock


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
	show_chart_buttons = blocks.BooleanBlock(default=False, required=False)
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

class CustomImageBlock(blocks.StructBlock):
	image = ImageChooserBlock(icon="image", required=True)
	align = blocks.ChoiceBlock(choices=[
		('left', 'Left'),
		('right', 'Right'),
		('full-width', 'Full Width')
	], required=True)
	width = blocks.ChoiceBlock([
		('auto', 'Auto'),
		('60%', '60%'),
		('50%', '50%'),
		('33.333%', '33%'),
		('25%', '25%')
	], default="auto", required=True)
	caption = blocks.TextBlock(required=False)
	source = blocks.TextBlock(required=False)

	class Meta:
		template = 'ui_elements/image_block.html'
