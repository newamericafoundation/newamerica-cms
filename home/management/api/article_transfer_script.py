import csv
import os
import urllib
import json
import datetime

from wagtail.wagtailimages.models import Image

from .newamerica_api_client import NAClient

from article.models import Article, ProgramArticlesPage

from django.utils.text import slugify
from django.core.files.images import ImageFile
from django.core.exceptions import ObjectDoesNotExist

from programs.models import Program

from weekly.models import Weekly, WeeklyEdition, WeeklyArticle

# Maps the program id from the old database API to the
# titles of the programs in the new database
mapped_programs = {
    '15': 'Asset Building',
    '7': 'Better Life Lab',
    '19': 'Cybersecurity Initiative',
    '13': 'Economic Growth',
    '5': 'Education Policy',
    '20': 'Family-Centered Social Policy',
    '1': 'Future of War',
    '9': 'Fellows',
    '2': 'Future Tense',
    '22': 'Global Cybersecurity Norms',
    '10': 'International Security',
    '8': 'New America DC',
    '24': 'New America CA',
    '17': 'New America Live',
    '18': 'New America NYC',
    '16': 'Open Markets',
    '3': 'Open Technology Institute',
    '6': 'Political Reform',
    '14': 'Post Secondary National Policy Institute',
    '21': 'Profits & Purpose',
    '23': 'Resilient Communities',
    '25': 'Resource Security',
    '12': 'New America Weekly',
    '4': 'Asset Building',
}


def get_post_date(original_date):
    """
    Takes the original date from the API
    and transforms it to fit the new database.
    If no date, it provides a default value.
    """
    if original_date:
        old_date_split = original_date.split("T")
        new_date = old_date_split[0]
    else:
        new_date = '2016-03-21'

    return new_date


def download_image(url, image_filename):
    """
    Takes the image URL from the old database API,
    retrieves the image and then saves it with a new
    filename
    """
    if url:
        image_location = os.path.join(
            'home/management/api/images',
            image_filename
        )
        urllib.urlretrieve(url, image_location)
        image = Image(
            title=image_filename,
            file=ImageFile(open(image_location), name=image_filename)
        )
        image.save()
        return image


def need_to_update_post(modified_date):
    """
    Takes in the modified date of the post and checks
    if it has been changes within the last 30 days
    and then updates the content as necessary
    """
    today = datetime.datetime.today()
    one_month_ago = today - datetime.timedelta(days=30)

    formatted_revision_date = get_post_date(modified_date)
    formatted_revision_date = datetime.datetime.strptime(
        formatted_revision_date, '%Y-%m-%d'
    )
    formatted_revision_date = formatted_revision_date.date()
    print(formatted_revision_date)

    if formatted_revision_date >= one_month_ago.date():
        return True


def load_weekly_mapping():
    """
    Opens the CSV of weekly content data and then
    loads and returns the necessary mapped fields
    """
    csv_data = {}
    with open('weekly_content.csv', "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            csv_data[str(row[0])] = {
                'edition_number': row[10],
            }
    return csv_data


def get_summary(old_summary):
    """
    Takes the original post summary from the API
    and transforms it to fit the new database.
    If no summary, it provides a default value.
    """
    if old_summary:
        return old_summary[:140]
    else:
        return "Summary goes here"


def load_articles():
    """
    Transfers all articles from the old database API
    for all programs excluding New America and New America Weekly
    into the new database creating objects of the Article model
    """
    for post, program_id in NAClient().get_articles():
        program_id = str(program_id)
        excluded_programs = ["12", "8"]
        # Leave out articles from New America DC and New America Weekly Programs
        if program_id not in excluded_programs:
            post_parent_program = Program.objects.get_or_create(
                title=mapped_programs[program_id])[0]

            parent_program_articles_homepage = post_parent_program\
                .get_children()\
                .type(ProgramArticlesPage)\
                .first()

            article_slug = slugify(post['title'])

            new_article = Article.objects.filter(slug=article_slug).first()

            # Only moves over published content
            if post['status'] == "published":
                # Checks that an article with this slug does not
                # exist already in the database and creates a new object
                if not new_article and article_slug:
                    new_article = Article(
                        search_description='',
                        seo_title='',
                        depth=4,
                        show_in_menus=False,
                        slug=article_slug,
                        title=post['title'],
                        date=get_post_date(post['publish_at']),
                        body=json.dumps([
                            {
                                'type': 'paragraph',
                                'value': post['content']
                            }
                        ]),
                        # story_excerpt=post['summary'],
                        story_image=download_image(
                            post['cover_image_url'],
                            post['title'] + "_image.jpeg"
                        )
                    )
                    print("Adding new article: ")
                    print(new_article)
                    parent_program_articles_homepage.add_child(
                        instance=new_article
                    )
                    new_article.save()
                # If the article does exist and has been modified within the
                # specified last number of days, it updates the fields 
                elif new_article and article_slug and need_to_update_post(post['modified']):
                    new_article.search_description = ''
                    new_article.seo_title = ''
                    new_article.depth = 4
                    new_article.show_in_menus = False
                    new_article.slug = article_slug
                    new_article.title = post['title']
                    new_article.date = get_post_date(post['publish_at'])
                    new_article.body = json.dumps([
                            {
                                'type': 'paragraph',
                                'value': post['content']
                            }
                    ]),
                    new_article.story_image = download_image(
                            post['cover_image_url'], 
                            post['title'] + "_image.jpeg"
                        )
                    print("Updating existing article: ")
                    print(new_article)
                    new_article.save()


def load_weekly_articles():
    """
    Transfers all New America Weekly articles from the old database API
    into the new database creating objects of the WeeklyArticle model.
    Also creates Weekly Editions if they do not exist.
    """
    weekly_mapping = load_weekly_mapping()

    weekly = Weekly.objects.first()

    for post in NAClient().get_weekly_articles():
        # Only moves over published content
        if post['status'] == "published":
            mapped_weekly_article = weekly_mapping[str(post['id'])]
        # Ensures content in the CSV with an edition number only is transferred
            if mapped_weekly_article['edition_number']:
                # Checking if Weekly Edition from the CSV exists, 
                # if it does not, creates that edition
                try:
                    weekly_edition = WeeklyEdition.objects.get(
                        title=mapped_weekly_article['edition_number']
                    )
                except ObjectDoesNotExist:
                    weekly_edition = WeeklyEdition(
                        title=mapped_weekly_article['edition_number'],
                        slug=slugify(
                            mapped_weekly_article['edition_number']
                        ),
                        depth=4
                    )
                    weekly.add_child(instance=weekly_edition)
                    weekly_edition.save()

                weekly_article_slug = slugify(post['title'])

                new_weekly_article = WeeklyArticle.objects.filter(
                    slug=weekly_article_slug
                ).first()
                # Checks that a new weekly article with this slug does not
                # exist already in the database and creates a new object
                if not new_weekly_article and weekly_article_slug:
                    new_weekly_article = WeeklyArticle(
                        search_description='',
                        seo_title='',
                        depth=5,
                        show_in_menus=False,
                        slug=weekly_article_slug,
                        title=post['title'],
                        date=get_post_date(post['publish_at']),
                        body=json.dumps([
                            {
                                'type': 'paragraph',
                                'value': post['content']
                            }
                        ]),
                        story_excerpt=get_summary(post['summary']),
                        story_image=download_image(
                            post['cover_image_url'],
                            post['title'] + "_image.jpeg"
                        )
                    )
                    print("Adding new article: ")
                    print(new_weekly_article)
                    weekly_edition.add_child(instance=new_weekly_article)
                    new_weekly_article.save()
                # If the object does exist and has been modified within the
                # specified last number of days, it updates the fields 
                elif new_weekly_article and weekly_article_slug and need_to_update_post(post['modified']):
                    new_weekly_article.search_description = ''
                    new_weekly_article.seo_title = ''
                    new_weekly_article.depth = 5
                    new_weekly_article.show_in_menus = False
                    new_weekly_article.slug = weekly_article_slug
                    new_weekly_article.title = post['title']
                    new_weekly_article.story_excerpt=get_summary(
                        post['summary']
                    )
                    new_weekly_article.date = get_post_date(
                        post['publish_at']
                    )
                    new_weekly_article.body = json.dumps([
                        {
                            'type': 'paragraph',
                            'value': post['content']
                        }
                    ]),
                    new_weekly_article.story_image = download_image(
                            post['cover_image_url'], 
                            post['title'] + "_image.jpeg"
                        )
                    print("Updating existing article: ")
                    print(new_weekly_article)
                    new_weekly_article.save()
