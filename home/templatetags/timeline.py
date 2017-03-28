from datetime import date
from django import template
from time import strptime

register = template.Library()

month_array = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

def get_date_display(date, datetype):
	if datetype == 'day':
		return month_array[date.month] + " " + str(date.day) + ", " + str(date.year)
	elif datetype == 'month':
		return month_array[date.month] + " " + str(date.year)
	else:
		return str(date.year)

@register.simple_tag()
def timeline_format_date(start_date, end_date, date_display_type):
	ret_string = get_date_display(start_date, date_display_type)

	if end_date:
		formatted_end_date = get_date_display(end_date, date_display_type)
		if formatted_end_date != ret_string:
			ret_string += " - " + formatted_end_date

	return ret_string

