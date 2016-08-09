from datetime import datetime, timedelta
from pytz import timezone
from django import template
from django.conf import settings
from programs.models import Program
from django.utils.safestring import mark_safe

from person.templatetags import tags as person_tags


register = template.Library()

@register.filter()
def get_range(num):
	if num:
		list_of_numbers = list(range(1, int(num)+1))

		return list_of_numbers

# generates appropriate list separators for list items (no oxford commas :) )
@register.simple_tag()
def list_separator(i):
	if i >= 2:
		return ", "
	elif i == 1:
		return " and "
	else:
		return ""


# handles pluralization for content labels across the site
@register.simple_tag()
def pluralize(num_items, label):
	if num_items > 1:
		return label + "s: "
	else:
		return label + ": "


# generates byline for all post types - calls byline prefix tag to get apporpriate prefix
@register.simple_tag()
def generate_byline(content_type, authors):
	return person_tags.generate_byline(content_type, authors)


# maps inernal content types to external content type display
@register.simple_tag()
def generate_content_type_line(ptype):
	page_type = str(ptype)

	page_mappings = {
		"program simple page" : "",
		"org simple page" : "",
		"Homepage for All People in NAF" : "",
		"Our People Page for Programs and Subprograms" : "",
		"Our People Page for Board of Directors, Central Staff, and Leadership Team" : "",
		"jobs page" : "",
		"subscribe page" : "",
		"Homepage for all Weekly Editions" : "",
		"issue or topic" : "",
		"Article and Op-Ed" : "Article",
		"redirect page": "",
	}

	if page_type in page_mappings:
		return page_mappings[page_type]
	else:
		return page_type


# generates date line for all post types/ datetime line for events
@register.simple_tag()
def generate_dateline(post):
	print(post)
	ret_string = ""
	date_format = '%B %-d, %Y'
	time_format = '%-I:%M %p'

	if str(post.content_type) == "event":
		if post.date:

			ret_string += '<p class="date">'
			ret_string += post.date.strftime(date_format)
			if post.end_date:
				if post.end_date != post.date:
					ret_string += ' - ' + post.end_date.strftime(date_format)
			ret_string += '</p>'

		if post.start_time:
			ret_string += '<p class="time">'
			ret_string += post.start_time.strftime(time_format).lower()
			if post.end_time:
				ret_string += ' - ' + post.end_time.strftime(time_format).lower()
			ret_string += '</p>'
	elif str(post.content_type) == "person":
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
	start_time = item.start_time
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
