import csv
import json

from .newamerica_api_client import NAClient

from blog.models import BlogPost, ProgramBlogPostsPage

import django.db.utils
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist

from weekly.models import Weekly, WeeklyEdition, WeeklyArticle

from transfer_script_helpers import download_image, get_post_date, get_summary, need_to_update_post, get_program, get_content_homepage, get_post_authors, connect_programs_to_post, get_subprogram, get_edcentral_date


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


def edcentral_blog_mapping():
    all_data = []
    csv_data = {}
    print("GOT HERE!")
    with open('edcentral3.csv', "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            csv_data[str(row[0])] = {
                'title': row[0],
                'link': row[1],
                'date': row[2],
                'author': row[3],
                'content': row[5]
            }
            all_data.append(csv_data[str(row[0])])
    return all_data


def load_education_blog_posts():
    """
    Transferring blog posts from EdCentral CSV
    for Education Policy Program
    """
    education_blog_mapping = edcentral_blog_mapping()

    for post in education_blog_mapping:
        if post['title'] == 'title':
            pass
        else:
            post_parent = get_program('5')
            parent_blog_homepage = get_content_homepage(
                post_parent, 
                ProgramBlogPostsPage,
                'EdCentral',
            )
            ed_blog_post_slug = slugify(post['title'])
            new_blog_post = BlogPost.objects.filter(slug=ed_blog_post_slug).first()
            
            if not new_blog_post and ed_blog_post_slug:
                new_blog_post = BlogPost(
                    search_description='',
                    seo_title='',
                    depth=5,
                    show_in_menus=False,
                    slug=ed_blog_post_slug,
                    title=post['title'],
                    date=get_edcentral_date(post['date']),
                    subheading='',
                    body=json.dumps([
                        {
                            'type': 'paragraph',
                            'value': post['content']
                        }
                    ]),
                )
                parent_blog_homepage.add_child(instance=new_blog_post)
                new_blog_post.save()
                print("-------------------ADDED NEW EDCENTRAL POST----------------------")
                get_post_authors(new_blog_post, post['author'])

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