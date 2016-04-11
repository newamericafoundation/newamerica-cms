import csv
import os
import urllib
import json
import datetime
import django.db.utils

from wagtail.wagtailimages.models import Image

from .newamerica_api_client import NAClient

from book.models import Book, ProgramBooksPage

from django.utils.text import slugify
from django.core.files.images import ImageFile
from django.core.exceptions import ObjectDoesNotExist

from programs.models import Program

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
    print(formatted_revision_date)

    if formatted_revision_date >= one_month_ago.date():
        return True


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


def load_books():
    """
    Transfers all books from the old database API
    for all programs into the new database
    creating objects of the Book model
    """
    for post, program_id in NAClient().get_books():
        if post['status'] == "published":
            try:
                program_id = str(program_id)
                print(program_id)
                post_parent_program = Program.objects.get_or_create(
                    title=mapped_programs[program_id], 
                    depth=3
                )[0]
                post_parent_program.save()
                parent_program_books_homepage = post_parent_program.get_children().type(ProgramBooksPage).first()

                book_slug = slugify(post['title'])

                new_book = Book.objects.filter(slug=book_slug).first()

                if not new_book and book_slug:
                    new_book = Book(
                        search_description='',
                        seo_title='',
                        depth=5,
                        show_in_menus=False,
                        slug=book_slug,
                        title=post['title'],
                        date=get_post_date(post['publish_at']),
                        publication_cover_image=download_image(
                            post['book_cover_image_url'], 
                            book_slug + "_cover_image.jpeg"
                        ),
                        subheading=post['sub_headline'],
                        body=json.dumps([
                            {
                                'type': 'paragraph',
                                'value': post['content']
                            }
                        ]),
                        story_excerpt=get_summary(post['summary']),
                        story_image=download_image(
                            post['cover_image_url'], 
                            book_slug + "_image.jpeg"
                        ),
                    )
                    print("Adding new book: ")
                    print(new_book)
                    parent_program_books_homepage.add_child(instance=new_book)
                    new_book.save()
                elif new_book and book_slug and need_to_update_post(post['modified']):
                    new_book.search_description = ''
                    new_book.seo_title = ''
                    new_book.depth = 5
                    new_book.date = get_post_date(post['publish_at'])
                    new_book.show_in_menus = False
                    new_book.slug = book_slug
                    new_book.title = post['title']
                    new_book.body = json.dumps([
                            {
                                'type': 'paragraph',
                                'value': post['content']
                            }
                        ])
                    new_book.publication_cover_image = download_image(
                            post['book_cover_image_url'], 
                            book_slug + "_cover_image.jpeg"
                        )
                    new_book.story_image = download_image(
                            post['cover_image_url'], 
                            book_slug + "_image.jpeg"
                    )
                    new_book.subheading=post['sub_headline']
                    print("Updating existing book: ")
                    print(new_book)
                    new_book.save()
            except django.db.utils.IntegrityError:
                pass
