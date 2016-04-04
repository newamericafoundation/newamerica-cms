# coding=utf-8
import sys
import csv
import os
import urllib
import json
import datetime

import django.db.utils
from django.utils.text import slugify
from django.core.files.images import ImageFile

from wagtail.wagtailimages.models import Image

from .newamerica_api_client import NAClient

from event.models import Event, ProgramEventsPage

from home.models import PostProgramRelationship

from programs.models import Program

if sys.version_info[0] < 3:
    reload(sys)  # noqa
    sys.setdefaultencoding('utf-8')

# Maps the program id from the old database API to the
# titles of the programs in the new database
mapped_programs = {
        '15': 'Asset Building',
        '7': 'Better Life Lab',
        '19': 'Cybersecurity Initiative',
        '13': 'Economic Growth',
        '5': 'Education Policy',
        '20': 'Family-Centered Social Policy',
        '1': 'Future of War',
        '9': 'Fellows',
        '2': 'Future Tense',
        '22': 'Global Cybersecurity Norms',
        '10': 'International Security',
        '8': 'New America DC',
        '24': 'New America CA',
        '17': 'New America Live',
        '18': 'New America NYC',
        '16': 'Open Markets',
        '3': 'Open Technology Institute',
        '6': 'Political Reform',
        '14': 'Post Secondary National Policy Institute',
        '21': 'Profits & Purpose',
        '23': 'Resilient Communities',
        '25': 'Resource Security',
        '12': 'New America Weekly',
        '4': 'Asset Building',
}


def get_publish_date(original_date):
    if original_date:
        old_date_split = original_date.split("T")
        new_date = old_date_split[0]
    else:
        new_date = '2016-03-21'

    return new_date


def load_events_mapping():
    csv_data = {}
    with open('event_addresses.csv', "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            csv_data[str(row[0])] = {
                'host_organization': row[5],
                'street_address': row[6],
                'city': row[7],
                'state': row[8],
                'zipcode': row[9]
            }
    return csv_data


def get_program(programs, post):
    """
    Gets the program from the new database
    using the program_id from the 
    old database API 
    """
    for old_program in programs:
        old_program = str(old_program)
        new_program = Program.objects.get_or_create(title=mapped_programs['old_program'],description=mapped_programs['old_program'], depth=3)
        relationship = PostProgramRelationship(program=new_program, post=post)
        relationship.save()


def get_event_data(post):
    """
    Takes content from the old database API and
    performs the necessary transformation for 
    the data to fit the new database. Adds the
    correct fields to a dictionary called event_data
    """
    event_mapping = load_events_mapping()

    mapped_event = event_mapping[str(post['id'])]

    event_data = {}

    # Transforms the former event start date 
    # and time or provides a default if they do not exist 
    if post['start_date']:
        event_data['date'] = post['start_date'].split(" ")[0]
        event_data['start_time'] = post['start_date'].split(" ")[1]
    else:
        event_data['date'] = get_publish_date(post['publish_at'])
        event_data['start_time'] = '10:00'

    # Transforms the former event end date 
    # and time or provides a default if they do not exist 
    if post['end_date']:
        event_data['end_date'] = post['end_date'].split(" ")[0]
        event_data['end_time'] = post['end_date'].split(" ")[1]
    else:
        event_data['end_date'] = '2016-03-01'
        event_data['end_time'] = '1:00'

    # Adds the former event rsvp link to event_data dictionary
    # or provides a default if it does not exist
    if post['rsvp_link']:
        event_data['rsvp_link'] = post['rsvp_link']
    else:
        event_data['rsvp_link'] = 'http://www.newamerica.org'

    # Adds the former event host organization to event_data dictionary
    # or provides a default if it does not exist
    if mapped_event['host_organization']:
        event_data['host_organization'] = mapped_event['host_organization']
    else:
        event_data['host_organization'] = 'New America'

    # Pulls the events former street address from the CSV
    # or provides a default if it does not exist
    if mapped_event['street_address']:
        event_data['street_address'] = mapped_event['street_address']
    else:
        event_data['street_address'] = '740 15th St NW #900'

    # Pulls the events former city from the CSV
    # or provides a default if it does not exist
    if mapped_event['city']:
        event_data['city'] = mapped_event['city']
    else:
        event_data['city'] = 'Washington'

    # Pulls the events former state from the CSV
    # or provides a default if it does not exist
    if mapped_event['state']:
        event_data['state'] = mapped_event['state']
    else:
        event_data['state'] = 'D.C.'

    # Pulls the events former zipcode from the CSV
    # or provides a default if it does not exist
    if mapped_event['zipcode']:
        event_data['zipcode'] = mapped_event['zipcode']
    else:
        event_data['zipcode'] = '20005'

    return event_data


def download_image(url, image_filename):
    """
    Takes the image URL from the old database API, 
    retrieves the image and then saves it with a new 
    filename
    """
    if url:
        image_location = os.path.join(
            'home/management/api/images',
            image_filename
        )
        urllib.urlretrieve(url, image_location)
        image = Image(
            title=image_filename,
            file=ImageFile(open(image_location), name=image_filename)
        )
        image.save()
        return image


def need_to_update_post(modified_date):
    """
    Takes in the modified date of the post and checks
    if it has been changes within the last 30 days
    and then updates the content as necessary
    """
    today = datetime.datetime.today()
    one_month_ago = today - datetime.timedelta(days=30)
    
    formatted_revision_date = get_publish_date(modified_date)
    formatted_revision_date = datetime.datetime.strptime(formatted_revision_date , '%Y-%m-%d')
    formatted_revision_date = formatted_revision_date.date()
    print(formatted_revision_date)

    if formatted_revision_date >= one_month_ago.date():
        return True


def load_events():
    """
    Goes through the events for each program and creates 
    or updates events as necessary using the data from the 
    event_data dictionary 
    """
    for post, program_id in NAClient().get_events():
        try:
            program_id = str(program_id)
            post_parent_program = Program.objects.get_or_create(title=mapped_programs[program_id], depth=3)[0]
            post_parent_program.save()
            parent_program_events_homepage = post_parent_program.get_children().type(ProgramEventsPage).first()

            event_slug = slugify(post['title'])

            new_event = Event.objects.filter(slug=event_slug).first()

            event_data = get_event_data(post)

            if not new_event and event_slug:
                new_event = Event(
                    search_description='',
                    seo_title='',
                    depth=5,
                    show_in_menus=False,
                    slug=event_slug,
                    title=post['title'],
                    date=event_data['date'],
                    end_date=event_data['end_date'],
                    start_time=event_data['start_time'],
                    end_time=event_data['end_time'],
                    host_organization=event_data['host_organization'],
                    street_address=event_data['street_address'],
                    city=event_data['city'],
                    state=event_data['state'],
                    zipcode=event_data['zipcode'],
                    rsvp_link=event_data['rsvp_link'],
                    body=json.dumps([{'type':'paragraph', 'value':post['content']}]),
                    story_image=download_image(
                        post['cover_image_url'], 
                        event_slug + "_image.jpeg"
                    )
                )
                print("Adding new event: ")
                print(new_event)
                parent_program_events_homepage.add_child(instance=new_event)
                new_event.save()
            elif new_event and event_slug and need_to_update_post(post['modified']):
                new_event.search_description = ''
                new_event.seo_title = ''
                new_event.depth = 5
                new_event.date = event_data['date']
                new_event.end_date = event_data['end_date']
                new_event.start_time = event_data['start_time']
                new_event.end_time = event_data['end_time']
                new_event.host_organization = event_data['host_organization']
                new_event.street_address = event_data['street_address']
                new_event.city = event_data['city']
                new_event.state = event_data['state']
                new_event.zipcode = event_data['zipcode']
                new_event.rsvp_link = event_data['rsvp_link']
                new_event.show_in_menus = False
                new_event.slug = event_slug
                new_event.title = post['title']
                new_event.body = json.dumps(
                    [{'type':'paragraph', 'value':post['content']}]
                )
                new_event.story_image=download_image(
                        post['cover_image_url'], 
                        event_slug + "_image.jpeg"
                )
                print("Updating existing event: ")
                print(new_event)
                new_event.save()
        except django.db.utils.IntegrityError:
            pass
