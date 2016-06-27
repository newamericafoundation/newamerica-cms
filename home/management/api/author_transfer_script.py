# coding=utf-8
import sys

from django.utils.text import slugify

from person.models import OurPeoplePage, Person

from .newamerica_api_client import NAClient

from .transfer_script_helpers import download_image, load_users_mapping

from .article_transfer_script import load_weekly_articles, load_general_blogs, load_asset_blogs

from .policy_paper_transfer_script import load_policy_papers

from .event_transfer_script import load_events

from .book_transfer_script import load_books

from .podcast_transfer_script import load_podcasts

from .press_release_transfer_script import load_press_releases

from .in_the_news_transfer_script import load_in_the_news

from .redirect import create_redirects, downloads_redirect

from .blog_transfer_script import load_education_blog_posts

from .transform_to_article import transform_itn_to_articles

our_people_page = OurPeoplePage.objects.first()

if sys.version_info[0] < 3:
    reload(sys)  # noqa
    sys.setdefaultencoding('utf-8')


def users_data_stream(endpoint):
    users = NAClient()
    for user_set in users.get_data(endpoint):
        for user in user_set['results']:
            yield user


def get_role_info(old_role):

    new_roles = {
        "staff": 'Central Staff',
        "board": 'Board Member',
        "fellow": 'Fellow',
        "alumni": 'External Author/Former Staff',
    }
    expert_roles = ['Fellow']
    role_info = {}

    if not old_role:
        role_info['role_title'] = 'External Author/Former Staff'
        role_info['expert'] = False
    else:
        role_info['role_title'] = new_roles.get(
            old_role[0],
            'External Author/Former Staff'
        )
        if role_info['role_title'] in expert_roles:
            role_info['expert'] = True
        else:
            role_info['expert'] = False

    return role_info


def load_authors():
    users_mapping = load_users_mapping()
    
    for user_api in users_data_stream('users'):
        mapped_user = users_mapping[str(user_api['id'])]
        if not mapped_user['duplicate'] and not mapped_user['delete']:
            mapped_user_title = '{0} {1}'.format(
                mapped_user['first_name'],
                mapped_user['last_name'])
            mapped_user_slug = slugify(mapped_user_title)
            print("id is: ")
            print(user_api['id'])
            db_user = Person.objects.filter(slug=mapped_user_slug).first()
        
            role_info = get_role_info(user_api['roles'])
            if not db_user and mapped_user_slug:
                db_user = Person(
                        search_description='',
                        seo_title='',
                        show_in_menus=False,
                        slug=mapped_user_slug,
                        title=mapped_user_title,
                        first_name=mapped_user['first_name'],
                        last_name=mapped_user['last_name'],
                        position_at_new_america=user_api['title'],
                        role=role_info['role_title'],
                        email=user_api['email'],
                        expert=role_info['expert'],
                        depth=4,
                        profile_image=download_image(
                            user_api['image'],
                            mapped_user_slug + "_person_image.jpeg"
                        ),
                        short_bio=user_api['short_bio'],
                        long_bio=user_api['long_bio'],
                    )
                our_people_page.add_child(instance=db_user)
                db_user.save()
                print("New user")
                print(db_user)
            elif db_user and mapped_user_slug:
                db_user.search_description = ''
                db_user.seo_title = ''
                db_user.show_in_menus = False
                db_user.slug = mapped_user_slug
                db_user.title = mapped_user_title
                db_user.first_name = mapped_user['first_name']
                db_user.last_name = mapped_user['last_name'] 
                db_user.position_at_new_america = user_api['title']
                db_user.role = role_info['role_title']
                db_user.email = user_api['email']
                db_user.expert = role_info['expert']
                db_user.depth = 4
                db_user.short_bio = user_api['short_bio']
                db_user.long_bio = user_api['long_bio']
                db_user.profile_image = download_image(
                    user_api['image'],
                    mapped_user_slug + "_person_image.jpeg"
                )
                print("Existing user")
                print(db_user)
                db_user.save()


def run():
    # print("Starting authors")
    # load_authors()
    # print("Ending authors")
    # print("Starting events")
    # load_events()
    # print("Ending events")
    # print("Starting weekly")
    # load_weekly_articles()
    # print("Ending weekly")
    # print("Starting books")
    # load_books()
    # print("Ending books")
    # print("Starting pp")
    # load_policy_papers()
    # print("Ending pp")
    # print("Starting podcasts")
    # load_podcasts()
    # print("Ending podcasts")
    # print("Starting press releases")
    # load_press_releases()
    # print("Ending press releases")
    # print("Starting in the news")
    # load_in_the_news()
    # print("Finished in the news !!!!!!")
    # load_general_blogs()
    # load_asset_blogs()
    # create_redirects()
    print("about to start!")
    # load_education_blog_posts()
    # downloads_redirect()
    transform_itn_to_articles()
