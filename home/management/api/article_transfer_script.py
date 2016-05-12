import csv
import json

from .newamerica_api_client import NAClient

from article.models import Article, ProgramArticlesPage

from blog.models import BlogPost, ProgramBlogPostsPage

import django.db.utils
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist

from weekly.models import Weekly, WeeklyEdition, WeeklyArticle

from transfer_script_helpers import download_image, get_post_date, get_summary, need_to_update_post, get_program, get_content_homepage, get_post_authors, connect_programs_to_post, get_subprogram


def load_weekly_mapping():
    """
    Opens the CSV of weekly content data and then
    loads and returns the necessary mapped fields
    """
    csv_data = {}
    with open('weekly_content.csv', "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            csv_data[str(row[0])] = {
                'edition_number': row[10],
            }
    return csv_data


def load_general_blog_mapping():
    """
    Opens the CSV of weekly content data and then
    loads and returns the necessary mapped fields
    """
    csv_data = {}
    with open('general_blogs.csv', "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            csv_data[str(row[0])] = {
                'program': row[7],
            }
    return csv_data


def load_asset_blog_mapping():
    """
    Opens the CSV of asset program blog posts content data and then
    loads and returns the necessary mapped fields
    """
    csv_data = {}
    with open('asset_blog.csv', "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            csv_data[str(row[0])] = {
                'initiative': row[8],
                'blog': row[9],
            }
    return csv_data


def load_general_blogs():
    """
    Used the old database API to retrieve articles 
    and then using cleaned CSV data, turns the
    appropriate content items into blog posts
    """
    general_blog_mapping = load_general_blog_mapping()

    for post, program_id in NAClient().get_general_blogs():
        if post['status'] == "published":
            post_id = str(post['id'])
            print(post_id)
            
            mapped_blog_post = general_blog_mapping.get(post_id, None)
            
            if mapped_blog_post:
                print(post['id'])
                print("found this id above in the csv - adding blog")
                
                mapped_programs = mapped_blog_post['program'].split(',')
                program_id = str(program_id)
                print('these are the mapped programs')
                print(mapped_programs)

                if program_id in mapped_programs:
                    print(program_id)
                    print("found program id above in the mapped programs")

                    post_parent = get_program(program_id)
                    parent_blog_homepage = get_content_homepage(
                        post_parent, 
                        ProgramBlogPostsPage,
                        'Our Blog',
                    )
                    general_blog_post_slug = post['slug']
                    general_blog_post = BlogPost.objects.filter(slug=general_blog_post_slug).first()
                    if not general_blog_post and general_blog_post_slug:
                        general_blog_post = BlogPost(
                            search_description='',
                            seo_title='',
                            depth=5,
                            show_in_menus=False,
                            slug=general_blog_post_slug,
                            title=post['title'],
                            date=get_post_date(post['publish_at']),
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
                                general_blog_post_slug + "_image.jpeg"
                            ),
                        )
                        parent_blog_homepage.add_child(instance=general_blog_post)
                        general_blog_post.save()
                        get_post_authors(general_blog_post, post['authors'])
                        connect_programs_to_post(general_blog_post, post['programs'])
                        print("----------------------ADDED NEW BLOG POST------")
                        print(post_id)

def load_asset_blogs():
    """
    Used the old database API to retrieve Asset Building
    articles and then using cleaned CSV data, turns the
    appropriate content items into blog posts
    """
    asset_blog_mapping = load_asset_blog_mapping()

    for post in NAClient().get_asset_blog_posts():
        if post['status'] == "published":
            post_id = str(post['id'])
            print(post_id)
            mapped_asset_blog_post = asset_blog_mapping.get(post_id, None)
            if mapped_asset_blog_post:
                if mapped_asset_blog_post['initiative']:
                    print("adding asset initiative blog")
                    print(mapped_asset_blog_post['initiative'])
                    post_parent = get_subprogram('Asset Building', mapped_asset_blog_post['initiative'])
                    parent_blog_homepage = get_content_homepage(
                        post_parent, 
                        ProgramBlogPostsPage,
                        mapped_asset_blog_post['blog'],
                    )
                    asset_blog_post_slug = post['slug']
                    new_blog_post = BlogPost.objects.filter(slug=asset_blog_post_slug).first()
                    if not new_blog_post and asset_blog_post_slug:
                        new_blog_post = BlogPost(
                            search_description='',
                            seo_title='',
                            depth=6,
                            show_in_menus=False,
                            slug=asset_blog_post_slug,
                            title=post['title'],
                            date=get_post_date(post['publish_at']),
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
                                asset_blog_post_slug + "_image.jpeg"
                            ),
                        )
                        parent_blog_homepage.add_child(instance=new_blog_post)
                        new_blog_post.save()
                        get_post_authors(new_blog_post, post['authors'])
                else:
                    print("adding asset blog")
                    print(post['id'])
                    post_parent = get_program('15')
                    parent_blog_homepage = get_content_homepage(
                        post_parent, 
                        ProgramBlogPostsPage,
                        'Our Blog',
                    )
                    asset_blog_post_slug = post['slug']
                    new_blog_post = BlogPost.objects.filter(slug=asset_blog_post_slug).first()
                    if not new_blog_post and asset_blog_post_slug:
                        new_blog_post = BlogPost(
                            search_description='',
                            seo_title='',
                            depth=5,
                            show_in_menus=False,
                            slug=asset_blog_post_slug,
                            title=post['title'],
                            date=get_post_date(post['publish_at']),
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
                                asset_blog_post_slug + "_image.jpeg"
                            ),
                        )
                        parent_blog_homepage.add_child(instance=new_blog_post)
                        new_blog_post.save()
                        get_post_authors(new_blog_post, post['authors'])

def load_weekly_articles():
    """
    Transfers all New America Weekly articles from the old database API
    into the new database creating objects of the WeeklyArticle model.
    Also creates Weekly Editions if they do not exist.
    """
    weekly_mapping = load_weekly_mapping()

    weekly = Weekly.objects.first()

    for post in NAClient().get_weekly_articles():
        # Only moves over published content
        if post['status'] == "published":
            mapped_weekly_article = weekly_mapping[str(post['id'])]
        # Ensures content in the CSV with an edition number only is transferred
            if mapped_weekly_article['edition_number']:
                # Checking if Weekly Edition from the CSV exists, 
                # if it does not, creates that edition
                try:
                    weekly_edition = WeeklyEdition.objects.get(
                        title=mapped_weekly_article['edition_number']
                    )
                except ObjectDoesNotExist:
                    weekly_edition = WeeklyEdition(
                        title=mapped_weekly_article['edition_number'],
                        slug=slugify(
                            mapped_weekly_article['edition_number']
                        ),
                        depth=4
                    )
                    weekly.add_child(instance=weekly_edition)
                    weekly_edition.save()

                weekly_article_slug = slugify(post['title'])

                new_weekly_article = WeeklyArticle.objects.filter(
                    slug=weekly_article_slug
                ).first()
                # Checks that a new weekly article with this slug does not
                # exist already in the database and creates a new object
                if not new_weekly_article and weekly_article_slug:
                    new_weekly_article = WeeklyArticle(
                        search_description='',
                        seo_title='',
                        depth=5,
                        show_in_menus=False,
                        slug=weekly_article_slug,
                        title=post['title'],
                        date=get_post_date(post['publish_at']),
                        body=json.dumps([
                            {
                                'type': 'paragraph',
                                'value': post['content']
                            }
                        ]),
                        story_excerpt=get_summary(post['summary']),
                        story_image=download_image(
                            post['cover_image_url'],
                            post['title'] + "_image.jpeg"
                        )
                    )
                    weekly_edition.add_child(instance=new_weekly_article)
                    new_weekly_article.save()
                    print(weekly_edition)
                    print(new_weekly_article)
                    # If the article does exist and has 
                    # been modified within the specified 
                    # last number of days, it updates the fields 
                elif new_weekly_article and weekly_article_slug and need_to_update_post(post['modified']):
                    new_weekly_article.search_description = ''
                    new_weekly_article.seo_title = ''
                    new_weekly_article.depth = 5
                    new_weekly_article.show_in_menus = False
                    new_weekly_article.slug = weekly_article_slug
                    new_weekly_article.title = post['title']
                    new_weekly_article.story_excerpt=get_summary(
                        post['summary']
                    )
                    new_weekly_article.date = get_post_date(
                        post['publish_at']
                    )
                    new_weekly_article.body = json.dumps([
                        {
                            'type': 'paragraph',
                            'value': post['content']
                        }
                    ])
                    new_weekly_article.story_image = download_image(
                            post['cover_image_url'], 
                            post['title'] + "_image.jpeg"
                        )
                    new_weekly_article.save()