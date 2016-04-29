from datetime import date
from django import template
from django.conf import settings
from programs.models import Program
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def get_range(num):
	if num:
		list_of_numbers = list(range(1, int(num)+1))

		return list_of_numbers

@register.simple_tag()
def list_separator(i):
	if i >= 2:
		return ", "
	elif i == 1:
		return " and "
	else:
		return ""

@register.simple_tag()
def pluralize(num_items, label):
	if num_items > 1:
		return label + "s: "
	else:
		return label + ": "

@register.simple_tag()
def get_byline_prefix(post_type, items_list):
	num_items = len(items_list)
	if str(post_type) == "podcast":
		return pluralize(num_items, "Host")
	elif str(post_type) == ("blog post" or "weekly article"):
		return "By "
	elif str(post_type) == "In The News Piece":
		return "In the News: "
	else:
		return pluralize(num_items, "Author")

@register.simple_tag()
def get_author_block_prefix(post_type, items_list):
	num_items = len(items_list)

	if str(post_type) == ("blog post" or "weekly article"):
		return pluralize(num_items, "Author")
	else:
		return get_byline_prefix(post_type, items_list)

@register.simple_tag()
def generate_content_type_line(ptype):
	page_type = str(ptype)

	page_mappings = {
		"program simple page" : "",
		"org simple page" : "",
		"Our People Page for Board of Directors, Central Staff, and Leadership Team" : "",
		"jobs page" : "",
		"subscribe page" : "",
		"Homepage for all Weekly Editions" : "",
		"issue or topic" : "",
		"Article and Op-Ed" : "Article",
	}

	if page_type in page_mappings:
		return page_mappings[page_type]
	else:
		return page_type

@register.simple_tag()
def generate_byline(ptype, authors):
	post_type = str(ptype)
	num_authors = len(authors)
	ret_string = ""

	if post_type == ("event" or post_type == "press release"):
		return ret_string

	ret_string += get_byline_prefix(post_type, authors)

	counter = 1
	for author in authors:
		ret_string += '<a href="' + author.author.url + '">' + author.author.first_name + ' ' + author.author.last_name + '</a>'
		ret_string += list_separator(num_authors - counter)
		counter += 1

	return mark_safe(ret_string)

@register.simple_tag()
def generate_dateline(post):
	ret_string = ""
	date_format = '%B %d, %Y'
	time_format = '%-I:%M %p'
	
	if str(post.content_type) == "event":
		if post.date:

			ret_string += '<p class="date">'
			ret_string += post.date.strftime(date_format)
			if post.end_date and (post.end_date != post.date):
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

