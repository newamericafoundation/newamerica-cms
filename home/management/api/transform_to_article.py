# coding=utf-8
import django.db.utils

import json

import csv
import json
import io

from blog.models import BlogPost, ProgramBlogPostsPage

from django.core.exceptions import ObjectDoesNotExist

from .newamerica_api_client import NAClient

from article.models import Article, ProgramArticlesPage

from quoted.models import Quoted

from django.utils.text import slugify
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from transfer_script_helpers import download_image, get_post_date, get_summary, need_to_update_post, get_post_authors, get_program, get_content_homepage, connect_programs_to_post

def inthenews_to_article_mapping():
    csv_data = {}
    with open('transformtoarticle.csv', "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            csv_data[str(row[0])] = {
                'id': row[0],
                'title': row[2],
                'slug': row[3],
                'programs-reference': row[7]
            }
    return csv_data


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


# def transform_itn_to_articles():
#     article_mapping = inthenews_to_article_mapping()

#     for item in article_mapping:
#         slug = article_mapping[item]['slug']
#         print(slug)
#         post = Quoted.objects.filter(slug=slug).first()
#         if post:
#             parent_program = post.get_ancestors()[2]
#             parent_program_articles_homepage = get_content_homepage(
#                     parent_program, 
#                     ProgramArticlesPage,
#                     'Articles',
#             )
#             new_post = Article(
#                 title=post.title,
#                 date=post.date,
#                 slug=post.slug,
#                 body=post.body,
#                 depth=5,
#                 programs=post.programs.all(),
#                 source=post.source,
#                 source_url=post.source_url,
#             )
#             parent_program_articles_homepage.add_child(new_post)
#             new_post.save()
#         else:
#             print('did not find post here')
#             break



def transform_itn_to_articles():
    article_mapping = inthenews_to_article_mapping()

    for item in article_mapping:
        #print article_mapping[item]['id']
        client = NAClient()
        post = client.get_one_in_the_news_piece(article_mapping[item]['id'])
        try:
                post_parent_program = get_program(program_id)
                
                parent_program_books_homepage = get_content_homepage(
                    post_parent_program, 
                    ProgramArticlesPage,
                    'Articles',
                )

                article_slug = slugify(post['title'])

                new_article = Article.objects.filter(slug=article_slug).first()

                if not new_article and article_slug:
                    new_article = Article(
                        search_description='',
                        seo_title='',3
                        depth=5,
                        show_in_menus=False,
                        slug=article_slug,
                        title=post['title'],
                        date=get_post_date(post['publish_at']),
                        publication_cover_image=download_image(
                            post['book_cover_image_url'], 
                            article_slug + "_cover_image.jpeg"
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
                            article_slug + "_image.jpeg"
                        ),
                    )
                    parent_program_books_homepage.add_child(instance=new_article)
                    new_article.save()
                    get_post_authors(new_article, post['authors'])
                    connect_programs_to_post(new_article, post['programs'])
                elif new_article and article_slug and need_to_update_post(post['modified']):
                    new_article.search_description = ''
                    new_article.seo_title = ''
                    new_article.depth = 5
                    new_article.date = get_post_date(post['publish_at'])
                    new_article.show_in_menus = False
                    new_article.slug = article_slug
                    new_article.title = post['title']
                    new_article.body = json.dumps([
                            {
                                'type': 'paragraph',
                                'value': post['content']
                            }
                        ])
                    new_article.publication_cover_image = download_image(
                            post['book_cover_image_url'], 
                            article_slug + "_cover_image.jpeg"
                        )
                    new_article.story_image = download_image(
                            post['cover_image_url'], 
                            article_slug + "_image.jpeg"
                    )
                    new_article.subheading=post['sub_headline']
                    new_article.save()
                    get_post_authors(new_article, post['authors'])
                    connect_programs_to_post(new_article, post['programs'])
            except django.db.utils.IntegrityError:
                pass
        break
