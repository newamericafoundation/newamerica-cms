from django.db import models
from django import forms

from wagtail.wagtailcore import blocks
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.wagtailcore.blocks import IntegerBlock

class CustomImageBlock(blocks.StructBlock):
	image = ImageChooserBlock(icon="image", required=True)
	align = blocks.ChoiceBlock(choices=[
		('left', 'Left'),
		('right', 'Right'),
		('full-width', 'Full Width')
	], required=True)
	width = blocks.ChoiceBlock([
		('initial', 'Auto'),
		('60%', '60%'),
		('50%', '50%'),
		('33.333%', '33%'),
		('25%', '25%')
	], default="initial", required=True)

	class Meta:
		template = 'blocks/image_block.html'

class ButtonBlock(blocks.StructBlock):
	button_text = blocks.CharBlock(required=True, max_length=50)
	button_link = blocks.URLBlock(required=True, default="https://www.")
	alignment = blocks.ChoiceBlock(choices=[
		('left-aligned', 'Left'),
		('center-aligned', 'Center')
	])

	class Meta:
		template = 'blocks/button.html'
		icon = 'radio-full'
		label = 'Button'

class IframeBlock(blocks.StructBlock):
	source_url = blocks.URLBlock(required=True)
	width = IntegerBlock(max_value=1050, help_text="The maximum possible iframe width is 1050")
	height = IntegerBlock()

	class Meta:
		template = 'blocks/iframe.html'
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
		template = 'blocks/dataviz.html'
		icon = 'site'
		label = 'Dataviz'

class TimelineEventBlock(blocks.StructBlock):
	title = blocks.CharBlock(required=True)
	description = blocks.RichTextBlock(required=False)
	category = blocks.CharBlock(required=False)
	start_date = blocks.DateBlock(required=True)
	end_date = blocks.DateBlock(required=False)
	image = ImageChooserBlock(required=False, help_text="If both image and video are entered, will display video - image will be hidden")
	video = EmbedBlock(required=False)
	

class TimelineBlock(blocks.StructBlock):
	title = blocks.CharBlock(required=False)
	subheading = blocks.RichTextBlock(required=False)
	time_scale = blocks.ChoiceBlock([
		('years', 'Years'),
		('months', 'Months'),
		('days', 'Days'),
	])
	event_categories = blocks.ListBlock(blocks.CharBlock(), required=False)
	event_list = blocks.ListBlock(TimelineEventBlock())

	class Meta:
		template = 'blocks/timeline.html'
		icon = 'site'
		label = 'Timeline'

class TwoColumnBlock(blocks.StructBlock):
    left_column = blocks.RichTextBlock()
    right_column = blocks.RichTextBlock()

    class Meta:
        template = 'blocks/two-column.html'

class IntegerChoiceBlock(blocks.ChoiceBlock):
    choices = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5','5'),
        ('6', '6')
    )

class PersonBlock(blocks.StructBlock):
    name = blocks.TextBlock(required=True)
    title = blocks.TextBlock(required=False, max_length=125, help_text="125 character limit")
    description = blocks.RichTextBlock(required=False)
    image = ImageChooserBlock(icon='image', required=False)
    twitter = blocks.URLBlock(required=False)

class PeopleBlock(blocks.StreamBlock):
    person = PersonBlock();

    class Meta:
        template = 'blocks/people.html'

class GoogleMapBlock(blocks.StructBlock):
    use_page_address = blocks.BooleanBlock(default=False, required=False, help_text="If selected, map will use the address already defined for this page, if applicable. For most posts besides events, this should be left unchecked and the form below should be completed.")
    street = blocks.TextBlock(required=False)
    city = blocks.TextBlock(required=False, default='Washington')
    state = blocks.TextBlock(required=False, default='D.C.')
    zipcode = blocks.TextBlock(required=False, default='200')

    class Meta:
        template = 'blocks/google_map.html'

class SessionTypesBlock(blocks.ChoiceBlock):
    choices = (
        ('panel', 'Panel'),
        ('lecture', 'Lecture'),
        ('break', 'Break'),
        ('meal', 'Meal'),
        ('reception','Reception'),
        ('registration', 'Registration')
    )

class SessionSpeakerBlock(blocks.StructBlock):
    name = blocks.TextBlock(required=True)
    title = blocks.TextBlock(required=False)

class SessionBlock(blocks.StructBlock):
    name = blocks.TextBlock()
    session_type = SessionTypesBlock()
    description = blocks.RichTextBlock(required=False)
    start_time = blocks.TimeBlock(required=False)
    end_time = blocks.TimeBlock(required=False)
    speakers = blocks.StreamBlock([
        ('speaker', SessionSpeakerBlock())
    ])
    archived_video_link = blocks.URLBlock(help_text="Enter youtube link after conference", required=False)

class SessionDayBlock(blocks.StructBlock):
	collapsible = blocks.BooleanBlock(help_text="Allow schedule sessions to expand and collapse", required=False, default=True)
	day = IntegerChoiceBlock(help_text="What day of the conference is this session on?", required=False, default=1)
	start_time = blocks.TimeBlock(required=False)
	end_time = blocks.TimeBlock(required=False)
	sessions = blocks.StreamBlock([
        ('session', SessionBlock())
    ])

class SessionsBlock(blocks.StreamBlock):
	days = SessionDayBlock()
	class Meta:
		template = 'blocks/schedule.html'

class Body(blocks.StreamBlock):
	introduction = blocks.RichTextBlock(icon="openquote")
	heading = blocks.CharBlock(classname='full title', icon="title")
	paragraph = blocks.RichTextBlock()
	inline_image = CustomImageBlock(icon='image')
	video = EmbedBlock(icon='media')
	table = TableBlock()
	button = ButtonBlock()
	iframe = IframeBlock(icon="link")
	dataviz = DatavizBlock(icon="code")
	timeline = TimelineBlock(icon="arrows-up-down")
	google_map = GoogleMapBlock(icon="site")

class PanelBlock(blocks.StructBlock):
	title = blocks.TextBlock()
	body = Body()

class PanelsBlock(blocks.StreamBlock):
	panel = PanelBlock(icon="doc-empty-inverse")

	class Meta:
		template='blocks/panels.html'

class BodyBlock(Body):
	schedule = SessionsBlock(help_text="1 to 2 day schedule of events", icon="date")
	people = PeopleBlock(help_text="Grid of people with short bios that appear on click", icon="group")
	panels = PanelsBlock(icon="list-ul")
	image = ImageChooserBlock(template='blocks/image_block.html', help_text='Legacy option. Consider using Inline Image instead.', icon="placeholder")
