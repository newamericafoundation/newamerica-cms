from datetime import date
from django import template
from django.conf import settings
from programs.models import Program
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag()
def list_separator(i):
	if i >= 2:
		return ", "
	elif i == 1:
		return " and "
	else:
		return ""

@register.filter()
def get_range(num):
	if num:
		list_of_numbers = list(range(1, int(num)+1))

		return list_of_numbers

@register.filter()
def pluralize(item):
	if len(item) > 1:
		return "s"
	else:
		return ""

def pluralize_label(num_items, label):
	if num_items > 1:
		return label + "s: "
	else:
		return label + ""

@register.simple_tag()
def generate_byline(type, authors):
	post_type = str(type)
	num_authors = len(authors)
	ret_string = ""
	
	if post_type == "event" or post_type == "press release":
		return ""
	elif post_type == "podcast":
		ret_string += pluralize_label(num_authors, "Host")
	elif post_type == "blog post":
		ret_string += "By "
	elif post_type == "In The News Piece":
		ret_string += "In the News: "
	else:
		ret_string += pluralize_label(num_authors, "Author")

	counter = 1
	for author in authors:
		ret_string += '<a href="' + author.url + '">' + author.first_name + ' ' + author.last_name + '</a>'
		ret_string += list_separator(num_authors - counter)
		counter += 1

	print ret_string
	return mark_safe(ret_string)

@register.simple_tag()
def generate_dateline(post):
	ret_string = ""
	date_format = '%B %d, %Y'
	time_format = '%-I:%M %p'

	
	if post.date:
		ret_string += '<p class="date">'
		ret_string += post.date.strftime(date_format)
		if post.end_date:
			ret_string += ' - ' + post.end_date.strftime(date_format)
		ret_string += '</p>'

	if post.start_time:
		ret_string += '<p class="time">'
		ret_string += post.start_time.strftime(time_format).lower()
		if post.end_time:
			ret_string += ' - ' + post.end_time.strftime(time_format).lower()
		ret_string += '</p>'

	return mark_safe(ret_string)

