from wagtail.wagtailcore import blocks
from mysite.blocks import BodyBlock

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
    	])),
    	('footnote_field', blocks.CharBlock(required=False))
	]), help_text="Specify the field(s) where values to display will be found.  References of type 'in-text' and 'image' can only display one field, 'list' and 'fact-box' can display multiple fields.")

	class Meta:
		template = './blocks/data_reference.html'
		icon = 'cogs'
		label = 'Data Reference'