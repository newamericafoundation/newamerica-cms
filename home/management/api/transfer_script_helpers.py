import sys
import csv
import os
import urllib
import json
import datetime

from wagtail.wagtailimages.models import Image

from .newamerica_api_client import NAClient

from article.models import Article, ProgramArticlesPage

from django.utils.text import slugify
from django.core.files.images import ImageFile

from home.models import PostProgramRelationship

from programs.models import Program

from person.models import Person

from home.models import PostAuthorRelationship

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
    '22': 'Cybersecurity Initiative',
    '10': 'International Security',
    '8': 'New America DC',
    '24': 'New America CA',
    '17': 'New America DC',
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


def get_summary(old_summary):
    """
    Takes the original post summary from the API
    and transforms it to fit the new database.
    If no summary, it provides a default value.
    """
    if old_summary:
        return old_summary[:140]
    else:
        return "Summary goes here"


def get_post_date(original_date):
    """
    Takes the original date from the API
    and transforms it to fit the new database.
    If no date, it provides a default value.
    """
    if original_date:
        old_date_split = original_date.split("T")
        new_date = old_date_split[0]
    else:
        new_date = '2016-03-21'

    return new_date


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


def load_users_mapping():
    csv_data = {}
    with open('home/management/api/csv_scripts/authors.csv', "r") as csvfile:
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


def get_post_authors(post, authors):
    author_mapping = load_users_mapping()

    for author in authors:
        author = str(author)
        author_data = author_mapping[author]
        print(author_data)
        author_object = Person.objects.get(
            first_name=author_data['first_name'], 
            last_name=author_data['last_name']
        )
        print(author_object)
        if author_object:
            relationship = PostAuthorRelationship.objects.create(
                author=author_object,
                post=post,
            )
            print(relationship)
            relationship.save()


def need_to_update_post(modified_date):
    """
    Takes in the modified date of the post and checks
    if it has been changes within the last 30 days
    and then updates the content as necessary
    """
    today = datetime.datetime.today()
    one_month_ago = today - datetime.timedelta(days=30)

    formatted_revision_date = get_post_date(modified_date)
    formatted_revision_date = datetime.datetime.strptime(
        formatted_revision_date, '%Y-%m-%d'
    )
    formatted_revision_date = formatted_revision_date.date()

    if formatted_revision_date >= one_month_ago.date():
        return True
