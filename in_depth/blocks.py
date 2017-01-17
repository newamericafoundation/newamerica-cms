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
