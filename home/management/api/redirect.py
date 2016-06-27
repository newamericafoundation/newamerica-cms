#coding=utf-8
#!/usr/bin/python
import sys

import csv
import json
import os

# Allow imports from above
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from newamerica_api_client import NAClient
from transfer_script_helpers import load_users_mapping

from wagtail.wagtailredirects.models import Redirect
from wagtail.wagtailcore.models import Page

from person.models import Person
from django.utils.text import slugify

# Mappping of program ids to slugs of programs on the current site
mapped_programs = {
    '15': 'asset-building',
    '7': 'better-life-lab',
    '19': 'cybersecurity-initiative',
    '13': 'economic-growth',
    '5': 'education-policy',
    '20': 'family-centered-social-policy',
    '1': 'future-of-war',
    '9': 'fellows',
    '2': 'future-tense',
    '22': 'cybersecurity-initiative',
    '10': 'international-security',
    '8': 'new-america',
    '24': 'ca',
    '17': 'live',
    '18': 'nyc',
    '16': 'open-markets',
    '3': 'oti',
    '6': 'political-reform',
    '14': 'postsecondary-national-policy-institute',
    '21': 'profits-purpose',
    '23': 'resilient-communities',
    '25': 'resource-security',
    '12': 'weekly',
    '4': 'asset-building',
}


# runs the redirect commands
def create_redirects():
    # post_redirect()
    user_redirects()


def user_redirects():
    """
    Using the CSV data and the old database API,
    the script determines the old and new URLS for
    user bios and then using the Wagtail Redirect model
    creates objects mapping the two together to handle the redirect
    """
    users_mapping = load_users_mapping()
    for user in NAClient().get_users():
        mapped_user = users_mapping[str(user['id'])]
        if not mapped_user['duplicate'] and not mapped_user['delete']:
            mapped_user_title = '{0} {1}'.format(
                mapped_user['first_name'],
                mapped_user['last_name'])
            mapped_user_slug = slugify(mapped_user_title)
            old_path = "/experts/" + mapped_user_slug
            print(old_path)
            new_page = Person.objects.filter(slug=mapped_user_slug).first()
            if new_page:
                new_redirect, created = Redirect.objects.get_or_create(
                    old_path=old_path
                )
                new_redirect.redirect_page = new_page
                print(new_redirect)
                new_redirect.save()


def post_redirect():
    """
    Using the the old database API and the posts endpoint,
    the script determines the old and new URLS for
    pages and then using the Wagtail Redirect model
    creates objects mapping the two together to handle the redirect
    """
    for post, _ in NAClient().get_posts():
        post_slug = post['slug']
        print(post_slug)
        new_page = Page.objects.filter(slug=post_slug).first()
        if new_page:
            for program in post['programs']:
                old_path = '/{0}/{1}'.format(
                    mapped_programs[str(program)], post_slug
                )
                new_redirect, created = Redirect.objects.get_or_create(
                    old_path=old_path
                )
                new_redirect.redirect_page = new_page
                print(new_redirect)
                new_redirect.save()
                print(old_path)


def downloads_redirect():
    """
    Using list of 404 links from the old downloads folder
    if the old site's s3 bucket, the script determines 
    the old and new URLS for pages and then using the Wagtail 
    Redirect model creates objects mapping the 
    two together to handle the redirect
    """
    for link in links:
        # Using the old link from the 25th index onward because we only need the relative path that starts from "/downloads..."
        print(link[25:])
        new_link = link.replace("http://", "https://s3.amazonaws.com/")

        new_redirect, created = Redirect.objects.get_or_create(old_path=link[25:])
        new_redirect.redirect_link = new_link
        print(new_redirect)
        new_redirect.save()