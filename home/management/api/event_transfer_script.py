# coding=utf-8
import sys
import csv
import json

import django.db.utils
from django.utils.text import slugify

from .newamerica_api_client import NAClient

from event.models import Event, ProgramEventsPage

from transfer_script_helpers import download_image, get_post_date, get_summary, need_to_update_post, get_program, get_content_homepage, connect_programs_to_post

if sys.version_info[0] < 3:
    reload(sys)  # noqa
    sys.setdefaultencoding('utf-8')


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
        event_data['date'] = get_post_date(post['publish_at'])
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


def load_events():
    """
    Goes through the events for each program and creates 
    or updates events as necessary using the data from the 
    event_data dictionary 
    """
    for post, program_id in NAClient().get_events():
        if post['status'] == "published":
            try:
                post_parent_program = get_program(program_id)
                
                parent_program_events_homepage = get_content_homepage(
                    post_parent_program, 
                    ProgramEventsPage,
                    'Events',
                )

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
                        subheading=post['sub_headline'],
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
                        soundcloud_url=post['soundcloud_url'],
                        story_image=download_image(
                            post['cover_image_url'], 
                            event_slug + "_image.jpeg"
                        ),
                        story_excerpt=get_summary(post['summary']),
                    )
                    parent_program_events_homepage.add_child(
                        instance=new_event
                    )
                    new_event.save()
                    connect_programs_to_post(new_event, post['programs'])
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
                    new_event.subheading=post['sub_headline']
                    new_event.body = json.dumps(
                        [{'type':'paragraph', 'value':post['content']}]
                    )
                    new_event.story_image=download_image(
                            post['cover_image_url'], 
                            event_slug + "_image.jpeg"
                    )
                    new_event.story_excerpt=get_summary(post['summary'])
                    new_event.soundcloud_url=post['soundcloud_url']
                    new_event.save()
                    connect_programs_to_post(new_event, post['programs'])
            except django.db.utils.IntegrityError:
                pass
