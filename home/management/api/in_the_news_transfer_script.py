import django.db.utils

import json

from .newamerica_api_client import NAClient

from quoted.models import Quoted, ProgramQuotedPage

from django.utils.text import slugify
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from transfer_script_helpers import download_image, get_post_date, get_summary, need_to_update_post, get_post_authors, get_program, get_content_homepage, connect_programs_to_post

def get_source(source):
    if source:
        return source


def get_source_url(source_url):
    validate = URLValidator()
    if source_url:
        try:
            validate(source_url)
            return source_url
        except ValidationError:
            pass


def load_in_the_news():
    """
    Transfers all in the news pieces from the old database API
    for all programs into the new database
    creating objects of the Quoted model
    """
    for post, program_id in NAClient().get_in_the_news():
        if post['status'] == "published":
            try:
                post_parent_program = get_program(program_id)
                
                parent_program_quoted_homepage = get_content_homepage(
                    post_parent_program, 
                    ProgramQuotedPage,
                    'In The News',
                )

                in_the_news_slug = slugify(post['title'])

                new_in_the_news = Quoted.objects.filter(slug=in_the_news_slug).first()

                if not new_in_the_news and in_the_news_slug:
                    new_in_the_news = Quoted(
                        search_description='',
                        seo_title='',
                        depth=5,
                        show_in_menus=False,
                        slug=in_the_news_slug,
                        title=post['title'],
                        date=get_post_date(post['publish_at']),
                        subheading=post['sub_headline'],
                        body=json.dumps([
                            {
                                'type': 'paragraph',
                                'value': post['content']
                            }
                        ]),
                        source=get_source(post['source']),
                        source_url=get_source_url(post['source_url']),
                        story_excerpt=get_summary(post['summary']),
                        story_image=download_image(
                            post['cover_image_url'], 
                            in_the_news_slug + "_image.jpeg"
                        ),
                    )
                    parent_program_quoted_homepage.add_child(instance=new_in_the_news)
                    new_in_the_news.save()
                    get_post_authors(new_in_the_news, post['authors'])
                    connect_programs_to_post(new_in_the_news, post['programs'])
                elif new_in_the_news and in_the_news_slug and need_to_update_post(post['modified']):
                    new_in_the_news.search_description = ''
                    new_in_the_news.seo_title = ''
                    new_in_the_news.depth = 5
                    new_in_the_news.date = get_post_date(post['publish_at'])
                    new_in_the_news.show_in_menus = False
                    new_in_the_news.slug = in_the_news_slug
                    new_in_the_news.title = post['title']
                    new_in_the_news.body = json.dumps([
                            {
                                'type': 'paragraph',
                                'value': post['content']
                            }
                        ])
                    new_in_the_news.source=get_source(post['source'])
                    new_in_the_news.source_url=get_source_url(post['source_url'])
                    new_in_the_news.story_image = download_image(
                            post['cover_image_url'], 
                            in_the_news_slug + "_image.jpeg"
                    )
                    new_in_the_news.subheading=post['sub_headline']
                    new_in_the_news.save()
                    get_post_authors(new_in_the_news, post['authors'])
                    connect_programs_to_post(new_in_the_news, post['programs'])
            except django.db.utils.IntegrityError:
                pass
