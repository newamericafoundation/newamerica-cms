import csv
import json

from .newamerica_api_client import NAClient

from article.models import Article, ProgramArticlesPage

from blog.models import BlogPost, ProgramBlogPostsPage

import django.db.utils
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist

from weekly.models import Weekly, WeeklyEdition, WeeklyArticle

from transfer_script_helpers import download_image, get_post_date, get_summary, need_to_update_post, get_program, get_content_homepage, get_post_authors, connect_programs_to_post


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


def load_blog_mapping():
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


def load_blogs():
    """
    Transfers program blog posts from the old database API
    for all programs into the new database 
    creating objects of the BlogPost model
    """
    blog_mapping = load_blog_mapping()

    for post, program_id in NAClient().get_articles():
        # Only moves over published content
        if post['status'] == "published":
            try:
                # Gets the mapped blog post from the CSV and its parent programs
                mapped_blog_post = blog_mapping[str(post['id'])]
                print("found it in the csv")
                print(post['id'])
                mapped_blog_parent_programs = mapped_blog_post['program'].split(',')
                if str(program_id) == str(mapped_blog_parent_programs[0]):
                    try:
                        print("program id is: ")
                        print(program_id)
                        print("mapped program id is: ")
                        print(mapped_blog_parent_programs[0])
                        print(post['id'])
                        print("we found a match!")
                        post_parent_program = get_program(program_id)
                        
                        parent_program_blog_homepage = get_content_homepage(
                            post_parent_program, 
                            ProgramBlogPostsPage,
                            'Our Blog',
                        )
                        blog_post_slug = slugify(post['title'])

                        new_blog_post = BlogPost.objects.filter(slug=blog_post_slug).first()

                        if not new_blog_post and blog_post_slug:
                            new_blog_post = BlogPost(
                                search_description='',
                                seo_title='',
                                depth=5,
                                show_in_menus=False,
                                slug=blog_post_slug,
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
                                    blog_post_slug + "_image.jpeg"
                                ),
                            )
                            parent_program_blog_homepage.add_child(instance=new_blog_post)
                            new_blog_post.save()
                            get_post_authors(new_blog_post, post['authors'])
                            connect_programs_to_post(new_blog_post, post['programs'])
                            print("added blog post")
                    except django.db.utils.IntegrityError:
                        print("integrity error")
                        pass
            except KeyError:
                print("didnt find in CSV - skipping")
                pass

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

def load_articles():
    """
    Transfers all articles from the old database API
    for all programs excluding New America and New America Weekly
    into the new database creating objects of the Article model
    """
    for post, program_id in NAClient().get_articles():
        program_id = str(program_id)
        excluded_programs = ["12", "8", "17"]
        # Leave out articles from New America DC 
        # and New America Weekly Programs
        if program_id not in excluded_programs:
            post_parent_program = get_program(program_id)
            parent_program_articles_homepage = get_content_homepage(
                    post_parent_program, 
                    ProgramArticlesPage,
                    'Articles',
                )

            article_slug = slugify(post['title'])

            new_article = Article.objects.filter(slug=article_slug).first()

            # Only moves over published content
            if post['status'] == "published":
                # Checks that an article with this slug does not
                # exist already in the database and creates a new object
                try:
                    if not new_article and article_slug:
                        new_article = Article(
                            search_description='',
                            seo_title='',
                            depth=5,
                            show_in_menus=False,
                            slug=article_slug,
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
                        parent_program_articles_homepage.add_child(
                            instance=new_article
                        )
                        new_article.save()
                        get_post_authors(new_article, post['authors'])
                    # If the article does exist and has 
                    # been modified within the specified 
                    # last number of days, it updates the fields 
                    elif new_article and article_slug and need_to_update_post(post['modified']):
                        new_article.search_description = ''
                        new_article.seo_title = ''
                        new_article.depth = 5
                        new_article.show_in_menus = False
                        new_article.slug = article_slug
                        new_article.title = post['title']
                        new_article.date = get_post_date(post['publish_at'])
                        new_article.body = json.dumps([
                                {
                                    'type': 'paragraph',
                                    'value': post['content']
                                }
                        ])
                        new_article.story_image = download_image(
                                post['cover_image_url'], 
                                post['title'] + "_image.jpeg"
                            )
                        new_article.story_excerpt=get_summary(post['summary'])
                        new_article.save()
                        get_post_authors(new_article, post['authors'])
                except django.db.utils.IntegrityError:
                    pass
