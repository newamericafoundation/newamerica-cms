from django.core.management.base import BaseCommand

from wagtail.core.models import Page
from wagtail.contrib.redirects.models import Redirect


class Command(BaseCommand):
    help = "Generates redirects for all pages in a section to themselves. Run this before moving a section of pages."

    def add_arguments(self, parser):
        parser.add_argument('path', help="The URL path prefix of the pages in the tree. This must include the homepage slug at the beginning (usually `/home`)")

    def handle(self, path, **options):
        pages = list(Page.objects.filter(url_path__startswith=path))

        if not pages:
            self.stdout.write("No pages match the given URL path prefix")
            return

        self.stdout.write(f"This will create redirects for {len(pages)} pages. Continue? [y/n]")
        should_continue = input()

        if should_continue != 'y':
            self.stdout.write("Quitting.")
            return

        for page in pages:
            site_id, site_root, path = page.get_url_parts()

            self.stdout.write(f"Saving redirect '{path}' to '{page.title}'")
            Redirect.objects.update_or_create(
                old_path=Redirect.normalise_path(path),
                site_id=site_id,
                defaults={
                    'redirect_page': page,
                }
            )
