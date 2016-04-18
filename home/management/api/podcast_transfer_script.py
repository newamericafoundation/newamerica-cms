import django.db.utils

import json

from .newamerica_api_client import NAClient

from podcast.models import Podcast, ProgramPodcastsPage

from django.utils.text import slugify

from transfer_script_helpers import download_image, get_post_date, get_summary, need_to_update_post, get_post_authors, get_program, get_content_homepage, download_document

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
                    new_policy_paper.save()
                    get_post_authors(new_podcast, post['authors'])
                elif new_policy_paper and policy_paper_slug and need_to_update_post(post['modified']):
                    new_policy_paper.search_description = ''
                    new_policy_paper.seo_title = ''
                    new_policy_paper.depth = 5
                    new_policy_paper.date = get_post_date(post['publish_at'])
                    new_policy_paper.show_in_menus = False
                    new_policy_paper.slug = policy_paper_slug
                    new_policy_paper.title = post['title']
                    new_policy_paper.body = json.dumps([
                            {
                                'type': 'paragraph',
                                'value': post['content']
                            }
                        ])
                    new_policy_paper.attachment=json.dumps(
                            get_attachments(
                                post['attachments'],
                                policy_paper_slug
                            )
                        )
                    new_policy_paper.paper_url=json.dumps(
                            get_attachment_url(
                                post['attachments']
                            )
                        )
                    new_policy_paper.publication_cover_image = download_image(
                            post['cover_image_url'], 
                            policy_paper_slug + "_cover_image.jpeg"
                        )
                    new_policy_paper.story_image = download_image(
                            post['cover_image_url'], 
                            policy_paper_slug + "_image.jpeg"
                    )
                    new_policy_paper.subheading=post['sub_headline']
                    new_policy_paper.save()
                    get_post_authors(new_policy_paper, post['authors'])
            except django.db.utils.IntegrityError:
                pass