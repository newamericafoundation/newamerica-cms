from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailembeds.blocks import EmbedBlock


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
	source_url = EmbedBlock(required=True)
	width = blocks.CharBlock(max_length=5)
	height = blocks.CharBlock(max_length=5)
	preserve_aspect = blocks.BooleanBlock(default=True, label="Preserve Aspect Ratio?", help_text="If checked, will preserve width-height ratio on smaller width screens, otherwise will maintain original height regardless of screen width")

	class Meta:
		template = './blocks/iframe.html'
		icon = 'form'
		label = 'Iframe'