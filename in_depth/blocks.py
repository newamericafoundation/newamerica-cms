from wagtail.wagtailcore import blocks
from mysite.blocks import BodyBlock

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
    		('string', 'Image'),
    		('number', 'Number (with thousands-place comma)'),
    		('percent', 'Percent'),
    		('string', 'Plain-text'),
    		('price', 'Price'),
			('rank', 'Rank'),
    	], default='string')),
    	('footnote_field', blocks.CharBlock(required=False))
	]), help_text="Specify the field where values to display will be found.")

	def get_context(self, value):
		context = super(DataReferenceBlock, self).get_context(value)
		context["fields_json"] = json.dumps(value["fields_to_display"])
		# print(value["fields_to_display"])
		# print(context["fields_json"])
		return context

	class Meta:
		template = './blocks/data_reference.html'
		icon = 'cogs'
		label = 'Data Reference'