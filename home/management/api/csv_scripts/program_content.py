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
            content.get('address'),
            content.get('location'),
            content.get('content'),
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

def program_posts():
    with open('weekly_content2.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'title', 'slug', 'url', 'publish_at', 'modified','authors', 'programs', 'type', 'deleted'])
        idx = 0
        for content in NAClient().program_content(12):
            writer.writerows(convert_to_csv(content))
            print(idx)
            idx += 1


def event_addresses():
    with open('event_addresses.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'title', 'address', 'location', 'content'])
        idx = 0
        for content in NAClient().get_events():
            writer.writerows(event_to_csv(content))
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


articles()