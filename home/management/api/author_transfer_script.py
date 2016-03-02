import json 
import sys

from django.utils.text import slugify
from django.core.files.images import ImageFile

from wagtail.wagtailimages.models import Image 

from person.models import OurPeoplePage, Person

our_people_page = OurPeoplePage.objects.first()

if sys.version_info[0] < 3:
	reload(sys)  # noqa
	sys.setdefaultencoding('utf-8')

def load_transformation():
	with open('home/management/api/author_cleanup.json', "r") as stream:
		return json.load(stream)

def read_json(json_file):
	with open(json_file, "r") as stream:
		return json.load(stream)

def load_authors():
	authors_data = read_json('home/management/api/authors.json')
	for idx, author in enumerate(authors_data['results']):
		if idx > 250:
			break
		found = Person.objects.filter(
			slug=slugify(author['full_name']))
		if not found:
			image = Image(title="rando_%s" % idx, file=ImageFile(open('home/management/api/anne.jpeg'), name="ann_%s.jpeg" % idx))
			image.save()

			person = Person(
				search_description='', 
 				seo_title='', 
 				show_in_menus=False,
 				slug=slugify(author['full_name']),
				title=author['full_name'], 
				name=author['full_name'], 
				position_at_new_america='Staff', 
				role='Staff',
				email='staff@staff.com',
				expert=False,
				depth=4,
				profile_image=image,
			)
			our_people_page.add_child(instance=person)
			person.save()
		

def run():
	load_authors()