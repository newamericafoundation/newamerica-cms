from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from newamericadotorg.blocks import Body, DatavizBlock, CustomImageBlock, IframeBlock

class CustomDataVizImageBlock(blocks.StructBlock):
	image = ImageChooserBlock(icon="image", required=False)
	align = blocks.ChoiceBlock(choices=[
		('center', 'Centered'),
		('left', 'Left'),
		('right', 'Right')
	], default='center', required=False)
	width = blocks.ChoiceBlock([
		('initial', 'Auto'),
		('width-133', 'Medium'),
		('width-166', 'Large'),
		('width-200', 'X-Large')
	], default="initial", required=False)
	use_original = blocks.BooleanBlock(required=False, help_text="check if you do not want image compressed. Should be checked for all figures.")
	figure_number = blocks.CharBlock(required=False, max_length=3)
	figure_title = blocks.CharBlock(required=False, max_length=100)
	open_image_on_click = blocks.BooleanBlock(default=False, required=False)

	class Meta:
		template = 'blocks/image_block.html'

class ReportDataVizBlock(DatavizBlock):
	static_image_fallback = CustomDataVizImageBlock(icon='image')

class BoxBody(blocks.StreamBlock):
	paragraph = blocks.RichTextBlock()
	inline_image = CustomImageBlock(icon='image')
	video = EmbedBlock(icon='media')
	iframe = IframeBlock(icon="link")
	dataviz = ReportDataVizBlock(icon="code")

class BoxBlock(blocks.StructBlock):
	title = blocks.TextBlock()
	body = BoxBody()

	class Meta:
		template = 'blocks/box.html'

class ReportBody(Body):
	dataviz = ReportDataVizBlock(icon="code")
	box = BoxBlock()

class ReportSectionBlock(blocks.StructBlock):
	title = blocks.TextBlock()
	hide_title = blocks.BooleanBlock(required=False)
	body = ReportBody()

class FeaturedReportSectionBlock(blocks.StructBlock):
	label = blocks.TextBlock(max_length=30, required=False)
	description = blocks.TextBlock(max_length=65, required=False)
	url = blocks.URLBlock(required=True, default="https://www.")
	type = blocks.ChoiceBlock(choices=[
		('Highlight', 'Highlight'),
		('Data Visualization', 'Data Visualization'),
		('Resource', 'Resource')
	])

class EndnoteBlock(blocks.StructBlock):
    number = blocks.TextBlock()
    note = blocks.RichTextBlock()
