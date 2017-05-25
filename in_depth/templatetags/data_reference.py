from django import template

import json

register = template.Library()

@register.simple_tag()
def get_footnote_index(full_list, curr_index):
	list_converted = json.loads(full_list)
	i = 0
	footnote_count = 0
	while i < curr_index:
		print(list_converted[i]['footnote_field'])
		if list_converted[i]['footnote_field'] and list_converted[i]['footnote_field'] != "":
			footnote_count = footnote_count + 1

		i = i + 1

	return footnote_count + 1
