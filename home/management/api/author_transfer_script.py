import sys

import csv
import os
import urllib

from django.utils.text import slugify
from django.core.files.images import ImageFile

from wagtail.wagtailimages.models import Image

from person.models import OurPeoplePage, Person

from .newamerica_api_client import NAClient

from .post_transfer_script import load_posts, education_posts

our_people_page = OurPeoplePage.objects.first()

if sys.version_info[0] < 3:
    reload(sys)  # noqa
    sys.setdefaultencoding('utf-8')


def load_users_mapping():
    csv_data = {}
    with open('home/management/api/authors.csv', "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            csv_data[str(row[0])] = {
                'first_name': row[2],
                'last_name': row[3],
                'duplicate': row[4],
                'merged_with': row[5],
                'delete': row[6]
            }
    return csv_data


def users_data_stream():
    users = NAClient()
    for user_set in users.get_data('users'):
        for user in user_set['results']:
            yield user


def download_image(url, image_filename):
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


def get_role_info(old_role):

    new_roles = {
        "staff": 'Staff',
        "board": 'Board Member',
        "fellow": 'New America Fellow',
        "alumni": 'External Author/Former Staff',
        "programfellow": 'Program Fellow',
    }
    expert_roles = ['Board Member', 'New America Fellow', 'Program Fellow']
    role_info = {}

    if not old_role:
        role_info['role_title'] = 'External Author/Former Staff'
        role_info['expert'] = False
    else:
        role_info['role_title'] = new_roles.get(
            old_role[0],
            'External Author/Former Staff'
        )
        if role_info['role_title'] in expert_roles:
            role_info['expert'] = True
        else:
            role_info['expert'] = False

    return role_info


def load_authors():

    users_mapping = load_users_mapping()
    
    for user_api in users_data_stream():
        mapped_user = users_mapping[str(user_api['id'])]
        if not mapped_user['duplicate'] and not mapped_user['delete']:
            mapped_user_title = '{0} {1}'.format(
                mapped_user['first_name'],
                mapped_user['last_name'])
            print(mapped_user_title)
            mapped_user_slug = slugify(mapped_user_title)
            db_user = Person.objects.filter(slug=mapped_user_slug).first()
        
        role_info = get_role_info(user_api['roles'])
        if not db_user or mapped_user_slug:
            db_user = Person(
                    search_description='', 
                    seo_title='', 
                    show_in_menus=False,
                    slug=mapped_user_slug,
                    title=mapped_user_title, 
                    first_name=mapped_user['first_name'], 
                    last_name=mapped_user['last_name'], 
                    position_at_new_america=user_api['title'],
                    role=role_info['role_title'],
                    email=user_api['email'],
                    expert=role_info['expert'],
                    depth=4,
                    profile_image=download_image(
                        user_api['image'],
                        mapped_user_slug + "_image.jpeg"
                    ),
                    short_bio=user_api['short_bio'],
                    long_bio=user_api['long_bio'],
                )
            our_people_page.add_child(instance=db_user)
            db_user.save()
        else:
            db_user.search_description=''
            db_user.seo_title=''
            db_user.show_in_menus=False
            db_user.slug=mapped_user_slug
            db_user.title=mapped_user_title
            db_user.first_name=mapped_user['first_name']
            db_user.last_name=mapped_user['last_name'] 
            db_user.position_at_new_america=user_api['title']
            db_user.role=role_info['role_title']
            db_user.email=user_api['email']
            db_user.expert=role_info['expert']
            db_user.depth=4
            db_user.short_bio=user_api['short_bio']
            db_user.long_bio=user_api['long_bio']

            db_user.profile_image=download_image(
                user_api['image'],
                mapped_user_slug + "_image.jpeg"
            )
            db_user.save()


def run():
    # load_authors()
    # load_posts()
    education_posts()
