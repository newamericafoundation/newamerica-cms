# coding=utf-8
import csv
import json
import io

from .newamerica_api_client import NAClient

from blog.models import BlogPost, ProgramBlogPostsPage

import django.db.utils
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist

from transfer_script_helpers import download_image, get_post_date, get_summary, need_to_update_post, get_program, get_content_homepage, get_post_authors, connect_programs_to_post, get_subprogram, connect_subprograms_to_post, get_education_authors

def edcentral_blog_mapping():
    all_data = []
    csv_data = {}
    with io.open('edcentral10.csv', "r", encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            csv_data[str(row[0])] = {
                'title': row[0],
                'author': row[3],
                'categories': row[4],
                'content': row[6],
                'real_date': row[9],
                'slug': row[11],
                'excerpt': row[12],
            }
            all_data.append(csv_data[str(row[0])])
    return all_data

def clean_subprograms_for_ed(subprograms):
    """ 
    Cleans up and transforms format of subprograms 
    from the CSV to be able to attach posts to
    the subprograms 
    """
    subprograms = subprograms.split(",")

    all_subprograms = []
    
    for subprogram in subprograms:
        all_subprograms.append(subprogram.strip())
    print(all_subprograms)
    return all_subprograms
    

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
            print(post['title'])
            post_parent = get_program('5')
            parent_blog_homepage = get_content_homepage(
                post_parent, 
                ProgramBlogPostsPage,
                'EdCentral',
            )
            ed_blog_post_slug = post['slug']
            print(ed_blog_post_slug)
            new_blog_post = BlogPost.objects.filter(slug=ed_blog_post_slug).first()
            
            if not new_blog_post and ed_blog_post_slug:
                new_blog_post = BlogPost(
                    search_description='',
                    seo_title='',
                    depth=5,
                    show_in_menus=False,
                    slug=ed_blog_post_slug,
                    title=post['title'],
                    date=post['real_date'],
                    body=json.dumps([
                        {
                            'type': 'paragraph',
                            'value': post['content']
                        }
                    ]),
                    story_excerpt=get_summary(post['excerpt']),
                )
                parent_blog_homepage.add_child(instance=new_blog_post)
                new_blog_post.save()
                print("-------------------ADDED NEW EDCENTRAL POST----------------------")
                get_education_authors(new_blog_post, post['author'])
                connect_subprograms_to_post(new_blog_post, clean_subprograms_for_ed(post['categories']))
            elif new_blog_post and ed_blog_post_slug:
                new_blog_post.search_description = ''
                new_blog_post.seo_title = ''
                new_blog_post.depth = 5
                new_blog_post.show_in_menus = False
                new_blog_post.slug = ed_blog_post_slug
                new_blog_post.title = post['title']
                new_blog_post.date = post['real_date']
                new_blog_post.body = json.dumps([
                        {
                            'type': 'paragraph',
                            'value': post['content']
                        }
                ])
                new_blog_post.story_excerpt = get_summary(post['excerpt'])
                get_education_authors(new_blog_post, post['author'])
                connect_subprograms_to_post(new_blog_post, clean_subprograms_for_ed(post['categories']))
                print("-------------------UPDATED EXISTING EDCENTRAL POST----------------------")
                new_blog_post.save()