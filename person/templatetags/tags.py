from django.utils.safestring import mark_safe

def get_author_url(author):
	return '<a href="' + author.author.url + '">' + author.author.title + '</a>'

def get_byline_prefix(content_type):
	if content_type == 'podcast':
		return "Contributor(s): "
	elif content_type == "In The News Piece":
		return "In the News: "
	else:
		return "By "


def generate_author_string(authors):
	authors = authors.order_by('pk')
	author_length = len(authors)
	if author_length == 1:
		return get_author_url(authors[0])
	elif author_length == 2:
		return get_author_url(authors[0]) + ' and ' + get_author_url(authors[1])
	else:
		author_string = ""
		for index, author in enumerate(authors):
			if index < author_length - 2:
				author_string += get_author_url(author) + ", "
			elif index == author_length - 2:
				author_string += get_author_url(author) + " and "
			else:
				author_string += get_author_url(author)
		return author_string


def generate_byline(content_type, authors):
	if authors:
		return mark_safe(get_byline_prefix(content_type) + generate_author_string(authors))
	else:
		return ""
	
