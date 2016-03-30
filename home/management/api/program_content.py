import csv
import json

from newamerica_api_client import NAClient


def convert_to_csv(content):
    yield [
            content.get('title'),
            content.get('slug'),
            content.get('url'),            
            content.get('authors'),
            content.get('programs'),
            content.get('type'),
    ]

def event_to_csv(content):
    yield [
            content.get('id'),
            content.get('title'),
            content.get('address'),
            content.get('location'),

    ]

def program_posts():
    with open('program_content.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['title', 'slug', 'url', 'authors', 'programs', 'type'])
        idx = 0
        for content in NAClient().program_content():
            writer.writerows(convert_to_csv(content))
            print(idx)
            idx += 1


def event_addresses():
    with open('event_addresses.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'title', 'address', 'location'])
        idx = 0
        for content in NAClient().get_events():
            writer.writerows(event_to_csv(content))
            print(idx)
            idx += 1

event_addresses()