import csv
import os
import urllib
import datetime

from wagtail.wagtailimages.models import Image
from wagtail.wagtaildocs.models import Document

from django.utils.text import slugify
from django.core.files import File
from django.core.files.images import ImageFile
from django.core.exceptions import ObjectDoesNotExist

from programs.models import Program

from person.models import Person

from home.models import PostAuthorRelationship, HomePage

home_page = HomePage.objects.first()

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


def get_program(program_id):
    """
    Gets the program from the new database
    using the program_id from the 
    old database API 
    """
    program_id = str(program_id)
    old_program = mapped_programs[program_id]
    try:
        program = Program.objects.get(title=old_program)
    except ObjectDoesNotExist:
        program = Program(
            name=old_program,
            title=old_program,
            slug=slugify(old_program),
            description=old_program,
            depth=3,
        )
        home_page.add_child(instance=program)
        program.save()
    return program


def get_content_homepage(program, content_homepage_type, page_title):
    content_homepage = program.get_children().type(content_homepage_type).first()
    if content_homepage:
        return content_homepage
    else:
        content_homepage = content_homepage_type(
            title=page_title,
            slug=slugify(page_title),
            depth=(program.depth + 1),
        )
        program.add_child(instance=content_homepage)
        content_homepage.save()
        return content_homepage


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
        try:
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
        except django.db.utils.IntegrityError:
            pass


def download_document(url, document_filename):
    """
    Takes the attached document URL from the old database API,
    retrieves the document, then saves it with a new
    filename and attaches it to the post
    """
    if url:
        document_location = os.path.join(
            'home/management/api/documents',
            document_filename
        )
        urllib.urlretrieve(url, document_location)
        document = Document(
            title=document_filename,
            file=File(open(document_location), name=document_filename)
        )
        document.save()
        return document.id


def load_users_mapping():
    csv_data = {}
    with open('authors.csv', "r") as csvfile:
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
        if author_data['first_name']:
            if not author_data['delete'] and not author_data['duplicate']:
                author_object = Person.objects.get(
                    first_name=author_data['first_name'], 
                    last_name=author_data['last_name']
                )
                if author_object:
                    try:
                        PostAuthorRelationship.objects.get(
                            author=author_object,
                            post=post,
                        )
                    except PostAuthorRelationship.DoesNotExist:
                        relationship = PostAuthorRelationship.objects.create(
                            author=author_object,
                            post=post,
                        )
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
