from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.core.models import Site
from wagtail.contrib.redirects.models import Redirect

from weekly.models import Weekly, WeeklyArticle, WeeklyEdition


def find_available_slug(parent, requested_slug):
    existing_slugs = set(
        parent.get_children()
        .filter(slug__startswith=requested_slug)
        .values_list("slug", flat=True)
    )
    slug = requested_slug
    number = 1

    while slug in existing_slugs:
        slug = requested_slug + "-" + str(number)
        number += 1

    return slug


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        weekly_index = Weekly.objects.get()
        site = Site.objects.get()

        # Move weekly articles into the index
        for article in WeeklyArticle.objects.all():
            print("moving article", article)
            Redirect.objects.create(
                old_path=Redirect.normalise_path(article.relative_url(site)),
                redirect_page=article,
            )

            # Find a slug that isn't taken under the index
            old_slug = article.slug
            article.slug = find_available_slug(weekly_index, article.slug)

            if article.slug != old_slug:
                print("changed article slug", old_slug, "=>", article.slug)
                article.save(update_fields=['slug'])

            article.move(weekly_index, pos='last-child')

        # Convert editions into redirects to weekly index
        for edition in WeeklyEdition.objects.all():
            print("deleting edition", edition)
            Redirect.objects.create(
                old_path=Redirect.normalise_path(edition.relative_url(site)),
                redirect_page=weekly_index,
            )

            edition.delete()
