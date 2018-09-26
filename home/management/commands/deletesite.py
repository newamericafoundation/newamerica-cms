from django.core.management.base import BaseCommand
from wagtail.core.models import Page, Site


class Command(BaseCommand):
    def handle(self, *args, **options):
        Site.objects.all().delete()
        Page.objects.all().delete()
