from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks



class ButtonBlock(blocks.StructBlock):
	button_text = blocks.CharBlock(required=True, max_length=25)
	button_link = blocks.URLBlock(required=True, default="https://www.")
	alignment = blocks.ChoiceBlock(choices=[
		('left', 'Left'),
		('center', 'Center')
	])

	class Meta:
		icon = 'radio-full'
		label = 'Button'