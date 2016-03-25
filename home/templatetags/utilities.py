from datetime import date
from django import template
from django.conf import settings
import math
from programs.models import Program

register = template.Library()

@register.simple_tag()
def listify(i):
	if i >= 2:
		return ","
	elif i == 1:
		return " and"
	else:
		return ""

@register.filter()
def get_range(num):
	if num:
		list_of_numbers = list(range(1, int(num)+1))

		return list_of_numbers

@register.filter()
def cutpoint_3_col(entries, col_number):
	num_entries = len(entries)
	num_per_col = math.ceil(num_entries/3.0)
	return int(num_per_col) * int(col_number)