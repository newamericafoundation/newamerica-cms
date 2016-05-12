from .newamerica_api_client import NAClient
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
    post_redirect()
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

            new_page = Person.objects.filter(slug=mapped_user_slug).first()
            if new_page:
                new_redirect, created = Redirect.objects.get_or_create(
                    old_path=old_path
                )
                new_redirect.redirect_page = new_page

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
                new_redirect.save()
                print(old_path)
