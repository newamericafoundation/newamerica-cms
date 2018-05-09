from django.db import models
from django import forms

from wagtail.wagtailcore import blocks
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.wagtailcore.blocks import IntegerBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailcore.rich_text import RichText
from wagtail.wagtailcore.blocks import stream_block

import home.models
from wagtail.wagtaildocs.models import Document
from wagtail.wagtailcore.models import Page

from operator import itemgetter, attrgetter
import json, datetime

class CustomJSONEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
			return obj.isoformat()
		elif isinstance(obj, RichText):
			return obj.__str__()
		elif isinstance(obj, stream_block.StreamValue):
			return obj.stream_data

		return json.JSONEncoder.default(self, obj)

class CustomImageBlock(blocks.StructBlock):
	image = ImageChooserBlock(icon="image", required=True)
	align = blocks.ChoiceBlock(choices=[
		('center', 'Centered'),
		('left', 'Left'),
		('right', 'Right')
	], default='center', required=True)
	width = blocks.ChoiceBlock([
		('initial', 'Auto'),
		('width-133', 'Medium'),
		('width-166', 'Large'),
		('width-200', 'X-Large')
	], default="initial", required=True)
	use_original = blocks.BooleanBlock(required=False, help_text="check if you do not want image compressed. Should be checked for all figures.")
	figure_number = blocks.CharBlock(required=False, max_length=3)
	figure_title = blocks.CharBlock(required=False, max_length=100)
	open_image_on_click = blocks.BooleanBlock(default=False, required=False)

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
	width = blocks.ChoiceBlock([
		('column-width', 'Column Width'),
		('full-width', 'Full Width')
	], default='year', required=False)
	show_chart_buttons = blocks.BooleanBlock(default=False, required=False)
	container_id = blocks.CharBlock(required=True)

	class Meta:
		template = 'blocks/dataviz.html'
		icon = 'site'
		label = 'Dataviz'


class ReportDataVizBlock(DatavizBlock):
	static_image_fallback = CustomImageBlock(icon='image')

def ResourceKitSerializer(r):
	resources = []
	for block in r.stream_data:
		d = {}
		block_type = block['type']
		value = block['value']

		for key, val in value.iteritems():
			if key == 'image' and val is not None:
				img = home.models.CustomImage.objects.get(pk=val)
				try:
					img = img.get_rendition('fill-200x200')
				except:
					img = img
				d['image'] = img.file.url
			elif key == 'resource':
				if block_type == 'post':
					pg = Page.objects.get(pk=val).specific
					d['url'] = pg.url
					if not getattr(d, 'image', False):
						img = getattr(pg, 'story_image', None)
						if img == None:
							img = getattr(pg, 'profile_image', None)
						if img:
							try:
								d['image'] = img.get_rendition('fill-200x200').file.url
							except:
								d['image'] = img.file.url

				elif block_type == 'external_resource':
					d['url'] = val
				else:
					d['url'] = Document.objects.get(pk=val).file.url
			else:
				d[key] = val
		resources.append(d)

	j = json.dumps(resources, ensure_ascii=False)
	return j

class ResourceKit(blocks.StructBlock):
	title = blocks.CharBlock(required=True)
	description = blocks.TextBlock(required=False)
	resources = blocks.StreamBlock([
		('post', blocks.StructBlock([
			('name', blocks.CharBlock(required=True)),
			('image', ImageChooserBlock(icon='image', required=False)),
			('description', blocks.RichTextBlock(required=False)),
			('resource', blocks.PageChooserBlock(required=True))
		], icon='redirect', label='Post')),
		('external_resource', blocks.StructBlock([
			('name', blocks.CharBlock(required=True)),
			('image', ImageChooserBlock(icon='image', required=False)),
			('description', blocks.RichTextBlock(required=False)),
			('resource', blocks.URLBlock(required=True))
		], icon='site', label='External resource')),
		('attachment', blocks.StructBlock([
			('name', blocks.CharBlock(required=True)),
			('image', ImageChooserBlock(icon='image', required=False)),
			('description', blocks.RichTextBlock(required=False)),
			('resource', DocumentChooserBlock(required=True))
		], icon='doc-full', label='Attachment'))
    ])

	def get_context(self, value):
		context = super(ResourceKit, self).get_context(value)
		context['resources'] = ResourceKitSerializer(value['resources'])
		return context

	class Meta:
		template = 'blocks/resource_kit.html'

def getJSCompatibleList(input_list, is_era, sort):
	if sort:
		sortedList = sorted(input_list, key=lambda member: member['start_date'])
	else:
		sortedList = input_list

	retList = []
	for i, item in enumerate(sortedList):
		curr_item = {}
		curr_item['id'] = i
		curr_item['title'] = item['title']
		if (not(is_era)):
			curr_item['italicize_title'] = item['italicize_title']
		curr_item['start_date'] = item['start_date'].isoformat()
		curr_item['date_display_type'] = item['date_display_type']
		if (item['end_date'] and item['end_date'] > item['start_date']):
			curr_item['end_date'] = item['end_date'].isoformat()
		if (not(is_era) and item['category']):
			curr_item['category'] = item['category']

		retList.append(curr_item)

	return retList

def PersonBlockSerializer(block_value):
	people = []
	for block in block_value.stream_data:
		d = {}
		value = block['value']

		for key, val in value.iteritems():
			if key == 'image':
				img = home.models.CustomImage.objects.get(pk=val)
				try:
					img = img.get_rendition('fill-200x200')
				except:
					img = img
				d['image'] = img.file.url
			else:
				d[key] = val
		people.append(d)

	j = json.dumps(people, ensure_ascii=False)
	return j


class TimelineEventBlock(blocks.StructBlock):
	title = blocks.CharBlock(required=True)
	italicize_title = blocks.BooleanBlock(default=False, required=False)
	description = blocks.RichTextBlock(required=False)
	category = blocks.CharBlock(required=False,)
	start_date = blocks.DateBlock(required=True)
	end_date = blocks.DateBlock(required=False)
	date_display_type = blocks.ChoiceBlock([
		('year', 'Year'),
		('month', 'Month'),
		('day', 'Day'),
	], default='year', help_text="Controls how specific the date is displayed")

class TimelineEraBlock(blocks.StructBlock):
	title = blocks.CharBlock(required=True)
	start_date = blocks.DateBlock(required=True)
	end_date = blocks.DateBlock(required=False)
	date_display_type = blocks.ChoiceBlock([
		('year', 'Year'),
		('month', 'Month'),
		('day', 'Day'),
	], default='year', help_text="Controls how specific the date is displayed")

class TimelineBlock(blocks.StructBlock):
	title = blocks.CharBlock(required=True)
	subheading = blocks.CharBlock(required=False)
	default_view = blocks.ChoiceBlock([
		('timeline', 'Timeline'),
		('list', 'List'),
	], default='timeline', required=False, help_text="Should the default view be a timeline or a list?")

	major_timeline_splits = blocks.ListBlock(TimelineEraBlock(), default='', required=False)
	event_eras = blocks.ListBlock(TimelineEraBlock(), default='', required=False)
	event_categories = blocks.ListBlock(blocks.CharBlock(), default='', required=False)
	event_list = blocks.ListBlock(TimelineEventBlock())
	def get_context(self, value):
		context = super(TimelineBlock, self).get_context(value)
		context["sorted_event_list"] = sorted(value["event_list"], key=lambda member: member['start_date'])
		context["settings_json"] = json.dumps({"eventList":getJSCompatibleList(value["event_list"], False, True), "defaultView": value["default_view"], "eraList":getJSCompatibleList(value["event_eras"], True, True), "splitList":getJSCompatibleList(value["major_timeline_splits"], True, False), "categoryList":value["event_categories"]})
		return context

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
	title = blocks.CharBlock(required=True)
	description = blocks.TextBlock(required=False)
	person = PersonBlock()

	def get_context(self, value):
		context = super(PeopleBlock, self).get_context(value)
		context['people'] = PersonBlockSerializer(value)
		return context

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

class SessionSpeakerBlock(blocks.StructBlock):
    name = blocks.TextBlock(required=True)
    twitter = blocks.URLBlock(required=False)
    title = blocks.TextBlock(required=False)

class SessionTypesBlock(blocks.ChoiceBlock):
    choices = (
        ('panel', 'Panel'),
        ('lecture', 'Lecture'),
        ('break', 'Break'),
        ('meal', 'Meal'),
        ('reception','Reception'),
        ('registration', 'Registration')
    )

def SessionsSerializer(s):
	sessions = []
	for block in s:
		d = {}
		value = block['value']

		for key, val in value.iteritems():
			if key == 'speakers':
				d['speakers'] = []
				for speakerBlock in val:
					speaker = {}
					for k, v in speakerBlock['value'].iteritems():
						speaker[k] = v
					d['speakers'].append(speaker)
			else:
				d[key] = val
		sessions.append(d)

 	return sessions

class SessionBlock(blocks.StructBlock):
    name = blocks.TextBlock(required=False)
    #session_type = SessionTypesBlock()
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
	days = SessionDayBlock(help_text='for multi-day events')
	def get_context(self, value):
		context = super(SessionsBlock, self).get_context(value)
		days = []
		for day in value.stream_data:
			days.append(SessionsSerializer(day['value']['sessions']))

		context['days'] = json.dumps(days, ensure_ascii=False)

		return context
	class Meta:
		template = 'blocks/schedule.html'

class Body(blocks.StreamBlock):
	introduction = blocks.RichTextBlock(icon="openquote")
	heading = blocks.CharBlock(classname='full title', icon="title", template="blocks/heading.html")
	paragraph = blocks.RichTextBlock()
	inline_image = CustomImageBlock(icon='image')
	video = EmbedBlock(icon='media')
	table = TableBlock()
	button = ButtonBlock()
	iframe = IframeBlock(icon="link")
	dataviz = DatavizBlock(icon="code")
	timeline = TimelineBlock(icon="arrows-up-down")
	google_map = GoogleMapBlock(icon="site")
	resource_kit = ResourceKit(icon="folder")

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

class PanelBlock(blocks.StructBlock):
	title = blocks.TextBlock()
	body = Body()

class ReportSectionBlock(blocks.StructBlock):
	title = blocks.TextBlock()
	body = ReportBody()

class PanelsBlock(blocks.StreamBlock):
	panel = PanelBlock(icon="doc-empty-inverse")

	class Meta:
		template='blocks/panels.html'

class BodyBlock(Body):
	#schedule = SessionsBlock(help_text="1 to 2 day schedule of events", icon="date")
	people = PeopleBlock(help_text="Grid of people with short bios that appear on click", icon="group")
	panels = PanelsBlock(icon="list-ul")
	image = ImageChooserBlock(template='blocks/image_block.html', help_text='Legacy option. Consider using Inline Image instead.', icon="placeholder")
