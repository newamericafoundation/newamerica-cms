import sys
import csv
import os
import urllib
import json
import datetime

from wagtail.wagtailimages.models import Image

from .newamerica_api_client import NAClient

from article.models import Article, ProgramArticlesPage
from event.models import Event, ProgramEventsPage

from django.utils.text import slugify
from django.core.files.images import ImageFile

from home.models import PostProgramRelationship

from programs.models import Program

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


def get_program(programs, post):
    for old_program in programs:
        old_program = str(old_program)
        new_program = Program.objects.get_or_create(title=mapped_programs['old_program'],description=mapped_programs['old_program'], depth=3)
        relationship = PostProgramRelationship(program=new_program, post=post)
        relationship.save()


def get_post_date(original_date):
    if original_date:
        old_date_split = original_date.split("T")
        new_date = old_date_split[0]
    else:
        new_date = '2016-03-21'

    return new_date


def download_image(url, image_filename):
    if url:
        image_location = os.path.join(
            'home/management/api/article_images',
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
    today = datetime.datetime.today()
    one_month_ago = today - datetime.timedelta(days=30)
    
    formatted_revision_date = get_post_date(modified_date)
    formatted_revision_date = datetime.datetime.strptime(formatted_revision_date , '%Y-%m-%d')
    formatted_revision_date = formatted_revision_date.date()
    print(formatted_revision_date)

    if formatted_revision_date >= one_month_ago.date():
        return True


def load_articles():
    for post, program_id in NAClient().get_articles():
        program_id = str(program_id)
        post_parent_program = Program.objects.get_or_create(title=mapped_programs[program_id])[0]

        parent_program_articles_homepage = post_parent_program.get_children().type(ProgramArticlesPage).first()

        article_slug = slugify(post['title'])

        new_article = Article.objects.filter(slug=article_slug).first()
        
        if not new_article and article_slug:
            new_article = Article(
                search_description='',
                seo_title='',
                depth=4,
                show_in_menus=False,
                slug=article_slug,
                title=post['title'],
                date=get_post_date(post['publish_at']),
                body=json.dumps([{'type':'paragraph', 'value':post['content']}]),
                story_exerpt=post['summary'],
                story_image=download_image(
                    post['cover_image_url'], 
                    post['title'] + "_image.jpeg"
                )
            )
            print("Adding new article: ")
            print(new_article)
            parent_program_articles_homepage.add_child(instance=new_article)
            new_article.save()
        elif new_article and article_slug and need_to_update_post(post['modified']):
            new_article.search_description=''
            new_article.seo_title=''
            new_article.depth=4
            new_article.show_in_menus=False
            new_article.slug=article_slug
            new_article.title=post['title']
            new_article.date=get_post_date(post['publish_at'])
            new_article.body=json.dumps(
                [{'type':'paragraph', 'value':post['content']}]
            )
            new_article.story_image=download_image(
                    post['cover_image_url'], 
                    post['title'] + "_image.jpeg"
                )
            print("Updating existing article: ")
            print(new_article)
            new_article.save()

def load_events():
    for post, program_id in NAClient().get_events():
        program_id = str(program_id)
        post_parent_program = Program.objects.get_or_create(title=mapped_programs[program_id])[0]

        parent_program_events_homepage = post_parent_program.get_children().type(ProgramEventsPage).first()

        event_slug = slugify(post['title'])

        new_event = Event.objects.filter(slug=article_slug).first()

        if not new_event and event_slug:
            new_event = Event(
                search_description='',
                seo_title='',
                depth=4,
                show_in_menus=False,
                slug=event_slug,
                title=post['title'],
                date=get_post_date(post['start_date']),
                end_date=,
                start_time=,
                end_time=,
                
                body=json.dumps([{'type':'paragraph', 'value':post['content']}]),
                story_exerpt=post['summary'],
                story_image=download_image(
                    post['cover_image_url'], 
                    post['title'] + "_image.jpeg"
                )
            )
            print("Adding new article: ")
            print(new_event)
            parent_program_articles_homepage.add_child(instance=nnew_event)
            new_event.save()
        elif new_event and event_slug and need_to_update_post(post['modified']):
            new_event.search_description=''
            new_event.seo_title=''
            new_event.depth=4
            new_event.show_in_menus=False
            new_event.slug=article_slug
            new_event.title=post['title']
            new_event.date=get_post_date(post['publish_at'])
            new_event.body=json.dumps(
                [{'type':'paragraph', 'value':post['content']}]
            )
            new_event.story_image=download_image(
                    post['cover_image_url'], 
                    post['title'] + "_image.jpeg"
                )
            print("Updating existing article: ")
            print(new_event)
            new_event.save()
