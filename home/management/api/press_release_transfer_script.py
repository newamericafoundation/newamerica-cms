import django.db.utils

import json

from .newamerica_api_client import NAClient

from press_release.models import PressRelease, ProgramPressReleasesPage

from django.utils.text import slugify

from transfer_script_helpers import download_image, get_post_date, get_summary, need_to_update_post, get_post_authors, get_program, get_content_homepage, download_document, connect_programs_to_post

def get_attachments(attachments, title):
    """
    If there are attachments, it iterates through them
    and moves them into the StreamField
    """
    if attachments:
        content = []
        for attachment in attachments:
            content.append(
                {
                    'type': 'attachment',
                    'value': download_document(
                        attachment['attachment_url'],
                        title
                        )
                }
            )
        return content


def load_press_releases():
    """
    Transfers all press releases from the old database API
    for all programs into the new database
    creating objects of the PressRelease model
    """
    for post, program_id in NAClient().get_press_releases():
        if post['status'] == "published":
            try:
                post_parent_program = get_program(program_id)
                
                parent_program_press_releases_homepage = get_content_homepage(
                    post_parent_program, 
                    ProgramPressReleasesPage,
                    'Press Releases',
                )

                press_release_slug = slugify(post['title'])

                new_press_release = PressRelease.objects.filter(slug=press_release_slug).first()

                if not new_press_release and press_release_slug:
                    new_press_release = PressRelease(
                        search_description='',
                        seo_title='',
                        depth=5,
                        show_in_menus=False,
                        slug=press_release_slug,
                        title=post['title'],
                        date=get_post_date(post['publish_at']),
                        subheading=post['sub_headline'],
                        body=json.dumps([
                            {
                                'type': 'paragraph',
                                'value': post['content']
                            }
                        ]),
                        attachment=json.dumps(
                            get_attachments(
                                post['attachments'],
                                press_release_slug
                            )
                        ),
                        story_excerpt=get_summary(post['summary']),
                        story_image=download_image(
                            post['cover_image_url'], 
                            press_release_slug + "_image.jpeg"
                        ),
                    )
                    parent_program_press_releases_homepage.add_child(instance=new_press_release)
                    new_press_release.save()
                    get_post_authors(new_press_release, post['authors'])
                    connect_programs_to_post(new_press_release, post['programs'])
                elif new_press_release and press_release_slug and need_to_update_post(post['modified']):
                    new_press_release.search_description = ''
                    new_press_release.seo_title = ''
                    new_press_release.depth = 5
                    new_press_release.date = get_post_date(post['publish_at'])
                    new_press_release.show_in_menus = False
                    new_press_release.slug = press_release_slug
                    new_press_release.title = post['title']
                    new_press_release.body = json.dumps([
                            {
                                'type': 'paragraph',
                                'value': post['content']
                            }
                        ])
                    new_press_release.attachment=json.dumps(
                            get_attachments(
                                post['attachments'],
                                press_release_slug
                            )
                        )
                    new_press_release.story_image = download_image(
                            post['cover_image_url'], 
                            press_release_slug + "_image.jpeg"
                    )
                    new_press_release.subheading=post['sub_headline']
                    new_press_release.save()
                    get_post_authors(new_press_release, post['authors'])
                    connect_programs_to_post(new_press_release, post['programs'])
            except django.db.utils.IntegrityError:
                pass