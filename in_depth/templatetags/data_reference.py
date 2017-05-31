from django import template

import json

register = template.Library()

# loops through field list, counting number of footnotes before current
@register.simple_tag()
def get_footnote_index(json_field_list, curr_index):
	field_list = json.loads(json_field_list)
	i = 0
	footnote_count = 0
	while i < curr_index:
		if field_list[i]['footnote_field'] and field_list[i]['footnote_field'] != "":
			footnote_count += 1
		i += 1

	return footnote_count + 1
