import csv
import os
import urllib
import json
import datetime
import django.db.utils

from wagtail.wagtailimages.models import Image

from .newamerica_api_client import NAClient

import author_transfer_script

from book.models import Book, ProgramBooksPage

from django.utils.text import slugify
from django.core.files.images import ImageFile
from django.core.exceptions import ObjectDoesNotExist

from programs.models import Program

from person.models import Person

from home.models import PostAuthorRelationship

from transfer_script_helpers import mapped_programs, download_image, get_post_date, get_summary, need_to_update_post, get_post_authors, get_program, get_content_homepage


def load_books():
    """
    Transfers all books from the old database API
    for all programs into the new database
    creating objects of the Book model
    """
    for post, program_id in NAClient().get_books():
        if post['status'] == "published":
            try:
                post_parent_program = get_program(program_id)
                
                parent_program_books_homepage = get_content_homepage(
                    post_parent_program, 
                    ProgramBooksPage,
                    'Books',
                )

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
                    get_post_authors(new_book, post['authors'])
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
                    get_post_authors(new_book, post['authors'])
            except django.db.utils.IntegrityError:
                pass
