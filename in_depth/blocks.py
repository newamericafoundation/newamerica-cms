from wagtail import blocks
from newamericadotorg.blocks import BodyBlock

import json

class CollapsibleBlock(blocks.StructBlock):
	hidden_by_default = BodyBlock()

	class Meta:
		template = 'blocks/collapsible.html'
		icon = 'arrow-down'
		label = 'Collapsible'

class PanelColorThemes(blocks.ChoiceBlock):
	choices = [
		('white', 'White'),
	    ('grey', 'Grey'),
	    ('black', 'Black')
	]

class PanelBody(BodyBlock):
	collapsible = CollapsibleBlock()

class DataReferenceBlock(blocks.StructBlock):
	fields_to_display = blocks.ListBlock(blocks.StructBlock([
		('field_name', blocks.CharBlock(required=True)),
		('label', blocks.CharBlock(required=False)),
    	('format', blocks.ChoiceBlock(choices=[
    		('date', 'Date'),
    		('number', 'Number (with thousands-place comma)'),
    		('percent', 'Percent'),
    		('string', 'Plain-text'),
    		('price', 'Price'),
			('rank', 'Rank'),
			('markdown', 'Rich-text'),
    	], default='string')),
    	('footnote_field', blocks.CharBlock(required=False))
	]), help_text="Specify the field where values to display will be found.")

	class Meta:
		template = './blocks/data_reference.html'
		icon = 'cogs'
		label = 'Data Reference'

class VideoDataReferenceBlock(blocks.StructBlock):
	field_name = blocks.CharBlock(required=True)
	host_site = blocks.ChoiceBlock(choices=[
		('youtube', 'Youtube'),
		('vimeo', 'Vimeo'),
	], default='youtube')

	class Meta:
		template = './blocks/video_data_reference.html'
		icon = 'cogs'
		label = 'Video Data Reference'
