import django.db.utils

import json

from .newamerica_api_client import NAClient

from podcast.models import Podcast, ProgramPodcastsPage

from django.utils.text import slugify

from transfer_script_helpers import get_post_date, get_summary, need_to_update_post, get_post_authors, get_program, get_content_homepage


def load_podcasts():
    """
    Transfers all podcasts from the old database API
    for all programs into the new database
    creating objects of the Podcast model
    """
    for post, program_id in NAClient().get_podcasts():
        if post['status'] == "published":
            try:
                post_parent_program = get_program(program_id)
                
                parent_program_podcasts_homepage = get_content_homepage(
                    post_parent_program, 
                    ProgramPodcastsPage,
                    'Podcasts',
                )

                podcast_slug = slugify(post['title'])

                new_podcast = Podcast.objects.filter(slug=podcast_slug).first()

                if not new_podcast and podcast_slug:
                    new_podcast = Podcast(
                        search_description='',
                        seo_title='',
                        depth=5,
                        show_in_menus=False,
                        slug=podcast_slug,
                        title=post['title'],
                        date=get_post_date(post['publish_at']),
                        subheading=post['sub_headline'],
                        body=json.dumps([
                            {
                                'type': 'paragraph',
                                'value': post['content']
                            }
                        ]),
                        soundcloud=json.dumps([
                            {
                                'type': 'soundcloud_embed',
                                'value': post['soundcloud_url']
                            }
                        ]),
                        story_excerpt=get_summary(post['summary']),
                    )
                    parent_program_podcasts_homepage.add_child(
                    	instance=new_podcast
                    )
                    new_podcast.save()
                    #get_post_authors(new_podcast, post['authors'])
                elif new_podcast and podcast_slug and need_to_update_post(post['modified']):
                    new_podcast.search_description = ''
                    new_podcast.seo_title = ''
                    new_podcast.depth = 5
                    new_podcast.date = get_post_date(post['publish_at'])
                    new_podcast.show_in_menus = False
                    new_podcast.slug = podcast_slug
                    new_podcast.title = post['title']
                    new_podcast.body = json.dumps([
                            {
                                'type': 'paragraph',
                                'value': post['content']
                            }
                        ])
                    new_podcast.soundcloud=json.dumps([
                            {
                                'type': 'soundcloud_embed',
                                'value': post['soundcloud_url']
                            }
                        ])
                    new_podcast.subheading=post['sub_headline']
                    new_podcast.save()
                    #get_post_authors(new_podcast, post['authors'])
            except django.db.utils.IntegrityError:
                pass
