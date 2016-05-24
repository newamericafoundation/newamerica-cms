#coding=utf-8
import sys

import csv
import json
import os
import sys

# Allow imports from above
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from newamerica_api_client import NAClient


def convert_to_csv(content):
    yield [
            content.get('id'),
            content.get('title'),
            content.get('slug'),
            content.get('url'),
            content.get('publish_at'),
            content.get('modified'),            
            content.get('authors'),
            content.get('programs'),
            content.get('type'),
            content.get('deleted'),
    ]


def event_to_csv(content):
    yield [
            content.get('id'),
            content.get('title'),
            content.get('location'),
    ]


def articles_to_csv(content):
    yield [
            content.get('id'),
            content.get('title'),
            content.get('slug'),
            content.get('published'),
            content.get('authors'),
            content.get('programs'),
            content.get('tags')
    ]


def in_the_news_to_csv(content):
    yield [
            content.get('id'),
            content.get('publish_at'),
            content.get('title'),
            content.get('slug'),
            content.get('published'),
            content.get('authors'),
            content.get('programs'),
            #content.get('content')
    ]


def user_to_csv(content):
    yield [
            content.get('id'),
            content.get('full_name'),
    ]

def program_posts():
    with open('weekly_content_5_4_16.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'title', 'slug', 'url', 'publish_at', 'modified','authors', 'programs', 'type', 'deleted'])
        idx = 0
        for content in NAClient().program_content(12):
            writer.writerows(convert_to_csv(content))
            print(idx)
            idx += 1


def event_addresses():
    with open('event_addresses-5-4-16.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'title', 'location'])
        idx = 0
        for content in NAClient().get_events():
            writer.writerows(event_to_csv(content))
            print(idx)
            idx += 1


def get_users():
    with open('users-5-4-16.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'full_name'])
        idx = 0
        for content in NAClient().get_users():
            writer.writerows(user_to_csv(content))
            print(idx)
            idx += 1


def articles():
    with open('all_articles.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'id', 
            'title', 
            'slug', 
            'published', 
            'authors',
            'programs',
            'tags'
        ])
        idx = 0
        for content in NAClient().get_articles():
            writer.writerows(articles_to_csv(content))
            print(idx)
            idx += 1


def get_in_the_news():
    with open('all_in_the_news.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'id', 
            'publish_at',
            'title', 
            'slug', 
            'published', 
            'authors',
            'programs',
            #'content'
        ])
        idx = 0
        for content in NAClient().get_in_the_news():
            writer.writerows(in_the_news_to_csv(content))
            print(idx)
            idx += 1



get_in_the_news()