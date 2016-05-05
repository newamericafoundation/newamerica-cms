import django.db.utils

import json

from .newamerica_api_client import NAClient

from policy_paper.models import PolicyPaper, ProgramPolicyPapersPage

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


def get_attachment_url(attachments):
    """
    If there are attachments, it iterates through them
    and transfer the attachment url into the new database
    """
    if attachments:
        urls = []
        for attachment in attachments:
            urls.append(
                {
                    'type': 'policy_paper_url',
                    'value': attachment['attachment_url'],
                }
            )
        return urls


def load_policy_papers():
    """
    Transfers all policy papers from the old database API
    for all programs into the new database
    creating objects of the PolicyPaper model
    """
    for post, program_id in NAClient().get_policy_papers():
        if post['status'] == "published":
            try:
                post_parent_program = get_program(program_id)
                
                parent_program_policy_papers_homepage = get_content_homepage(
                    post_parent_program, 
                    ProgramPolicyPapersPage,
                    'Policy Papers',
                )

                policy_paper_slug = slugify(post['title'])
                print(post['id'])

                new_policy_paper = PolicyPaper.objects.filter(slug=policy_paper_slug).first()

                if not new_policy_paper and policy_paper_slug:
                    new_policy_paper = PolicyPaper(
                        search_description='',
                        seo_title='',
                        depth=5,
                        show_in_menus=False,
                        slug=policy_paper_slug,
                        title=post['title'],
                        date=get_post_date(post['publish_at']),
                        publication_cover_image=download_image(
                            post['cover_image_url'], 
                            policy_paper_slug + "_cover_image.jpeg"
                        ),
                        subheading=post['sub_headline'],
                        body=json.dumps([
                            {
                                'type': 'paragraph',
                                'value': post['content']
                            }
                        ]),
                        paper_url=json.dumps(
                            get_attachment_url(
                                post['attachments']
                            )
                        ),
                        attachment=json.dumps(
                            get_attachments(
                                post['attachments'],
                                policy_paper_slug
                            )
                        ),
                        story_excerpt=get_summary(post['summary']),
                        story_image=download_image(
                            post['cover_image_url'], 
                            policy_paper_slug + "_image.jpeg"
                        ),
                    )
                    parent_program_policy_papers_homepage.add_child(instance=new_policy_paper)
                    print("adding new paper")
                    print(post['id'])
                    new_policy_paper.save()
                    get_post_authors(new_policy_paper, post['authors'])
                    connect_programs_to_post(new_policy_paper, post['programs'])
                elif new_policy_paper and policy_paper_slug and need_to_update_post(post['modified']):
                    print("updating existing paper")
                    print(post['id'])
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
                    connect_programs_to_post(new_policy_paper, post['programs'])
            except django.db.utils.IntegrityError:
                pass