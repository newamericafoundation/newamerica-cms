import json
import math
from datetime import datetime, timedelta

from pytz import timezone
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from wagtail.core.blocks import StreamValue

from event.models import Event
from person.models import Person
from programs.models import Program


register = template.Library()

@register.filter()
def get_range(num):
	if num:
		list_of_numbers = list(range(1, int(num)+1))

		return list_of_numbers


@register.filter()
def has_rendition(img):
	return True if getattr(img, 'get_rendition', False) else False

# generates appropriate list separators for list items (no oxford commas :) )
@register.simple_tag()
def list_separator(i, length):
	if i >= 2:
		return "<span class='punc'>,&nbsp;</span>"
	elif length == 2 and i == 1:
		return "<span class='punc'>&nbsp;and&nbsp;</span>"
	elif i == 1:
		return "<span class='punc'>,&nbsp;and&nbsp;</span>"
	else:
		return ""


# this function is to support old inline image block width values
@register.filter()
def temp_image_width_map(width):
	if width == '60%':
		return 'width-200'
	if width == '50%':
		return 'width-166'
	if width == '33.333%':
		return 'width-133'
	return width

@register.filter()
def ellipsize(text, max_length):
	if len(text) > max_length:
		return text[:max_length].strip() + ' ...'

	return text


# handles pluralization for content labels across the site
@register.simple_tag()
def pluralize(num_items, label):
	if num_items > 1:
		return label + "s "
	else:
		return label + " "


# generates byline for all post types - calls byline prefix tag to get apporpriate prefix
@register.simple_tag()
def generate_byline(post_type, authors):
	authors = authors.select_related('author')
	num_authors = len(authors)
	ret_string = ""

	# events and press releases have no authors and therefore no byline
	if post_type == "event.Event" or post_type == "press_release.PressRelease":
		return ret_string

	# counter is used to determine appropriate list separator
	counter = 1
	for author in authors:
		ret_string += '<h4 class="inline margin-0 link"><a href="' + author.author.url + '"><u>' + author.author.first_name + ' ' + author.author.last_name + '</u></a></h4>'
		ret_string += list_separator(num_authors - counter, num_authors)
		counter += 1

	return mark_safe(ret_string)


# generates date line for all post types/ datetime line for events
@register.simple_tag()
def generate_dateline(post):
	ret_string = ""
	date_format = '%b. %-d, %Y'
	time_format = '%-I:%M %p'

	if issubclass(post.specific_class, Event):
		if post.date:
			ret_string += post.date.strftime(date_format)
			if post.end_date:
				if post.end_date != post.date:
					ret_string += ' - ' + post.end_date.strftime(date_format)

		if post.start_time:
			ret_string += '<br/>'
			ret_string += post.start_time.strftime(time_format).lower()
			if post.end_time:
				ret_string += ' - ' + post.end_time.strftime(time_format).lower()
	elif issubclass(post.specific_class, Person):
		return ""
	else:
		if post.date:
			ret_string += '<p class="date">' + post.date.strftime(date_format) + '</p>'

	return mark_safe(ret_string)

# calls helper function to determine if date/time are future or past, depending if event is single day or multi-day
# 	- single day events are considered past at the start time on the day of the event (start_date + start_time)
# 	- multi-day events are considered past at the start time on the final day of the event (end_date + start_time)
@register.filter
def is_future(item):
	if getattr(item, 'start_time', None):
		start_time = item.start_time
	else:
		start_time = datetime.min.time()

	start_date = item.date
	end_date = item.end_date


	if (end_date):
		return is_datetime_future(start_time, end_date)
	else:
		return is_datetime_future(start_time, start_date)


# helper function that compares date/time to current date/time to determine if event is past or future
def is_datetime_future(start_time, date):
	eastern = timezone('US/Eastern')
	curr_time = datetime.now(eastern).time()
	curr_date = datetime.now(eastern).date()

	if (date > curr_date):
		# date is future
		return 1
	elif (date == curr_date):
		# date is today, checking start time
		if (start_time >= curr_time):
			# start time is future
			return 1
		else:
			# start time is past
			return 0
	else:
		# date is past
		return 0


@register.simple_tag()
def person_display_contact_info(page):
	if (page.email):
		if (page.role != "External Author/Former Staff"):
			return 1

	return 0

@register.simple_tag()
def check_oti(path):
	path_pieces = path.split("/")

	if (path_pieces[1] == "oti"):
		return "oti"

	return ""


@register.filter
def noShowTableauHome(src):
        is_tableau = src.find('tableausoftware.com') != -1
        if is_tableau:
                has_showHome = src.find(':showVizHome=') != -1
                if not has_showHome:
                        qryIndex = src.find('?')
                        if qryIndex == -1: qryIndex = len(src)
                        return src[:qryIndex] + "?:showVizHome=no&" + src[qryIndex+1:]
                else:
                        return src

        return src

@register.simple_tag()
def group_by(key, items):
	groups = {}

	for item in items:

		if isinstance(item, StreamValue.StreamChild):
			i = item.value
		else:
			i = item

		if i[key] not in groups:
			groups[i[key]] = []

		groups[i[key]].append(item)

	return groups

# for google maps template, get location from the `location` object, Page data or GoogleMapBlock data
@register.simple_tag()
def get_location_data(passed_location,value,page):
	if passed_location:
		return passed_location
	if value.get('use_page_address', None):
		return page
	return value

from django.template.loader import render_to_string
from wagtail.embeds import embeds
from wagtail.embeds.exceptions import EmbedException

@register.simple_tag()
def oembed(url):
    try:
        embed = embeds.get_embed(url)

        # Work out ratio
        if embed.width and embed.height:
            ratio = str(embed.height / embed.width * 100) + "%"
        else:
            ratio = "0"

        # Render template
        return render_to_string('wagtailembeds/embed_frontend.html', {
            'embed': embed,
            'ratio': ratio,
        })
    except EmbedException:
        # silently ignore failed embeds, rather than letting them crash the page
        return ''

@register.simple_tag()
def split_program_list(start_list, max_size=6):
    final_list = []
    temp_list = []
    add = max_size
    length = len(start_list)
    for i, item in enumerate(start_list):
        if i+1 > max_size:
            max_size += add
            final_list.append(temp_list)
            temp_list = []
        elif i+1 == length:
            temp_list.append(item)
            final_list.append(temp_list)
            break

        temp_list.append(item)

    return final_list

@register.simple_tag()
def group_programs(programs, cols=3):
	length = len(programs)
	l = length/float(cols)
	max_items = math.ceil(l)

	groups = []
	for i in range(cols):
		groups.append([])

	group_index = 0
	for i, p in enumerate(programs):
		groups[group_index].append(p)
		if (i+1) % max_items == 0:
			group_index += 1

	return groups

@register.tag()
def counter(parser, token):
    """
    Counter tag. Can be used to output and increment a counter.

    Usage:
    - {% counter %} to output and post-increment the counter variable
    - {% counter reset %} to reset the counter variable to 1
    - {{ counter_var %} to access the last counter variable without incrementing

    """
    try:
        tag_name, reset = token.contents.split(None, 1)
    except ValueError:
        reset = False
    else:
        if reset == 'reset':
            reset = True
    return CounterNode(reset)

class CounterNode(template.Node):
    def __init__(self, reset):
        self.reset = reset

    def render(self, context):
        # When initializing or resetting, set counter variable in render_context to 1.
        if self.reset or ('counter' not in context.render_context):
            context.render_context['counter'] = 1

        # Set the counter_var context variable
        context['counter_var'] = context.render_context['counter']

        # When resetting, we don't want to return anything
        if self.reset:
            return ''

        # Increment counter. This does not affect the return value!
        context.render_context['counter'] += 1

        # Return counter number
        return context['counter_var']


@register.filter
def model_name(page):
	"""
	Gets the model name of the page in the form 'app_name.ModelName'
	"""
	return page._meta.app_label + '.' + page.__class__.__name__


@register.filter
def model_display_name(page):
	"""
	Gets verbose name of the page's model
	"""
	if isinstance(page, str):
		return
	if page._meta.verbose_name.title() == 'Other Post':
		return page.other_content_type
	else:
		return page._meta.verbose_name.title()
