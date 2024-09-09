from django.core.management.base import BaseCommand
from subscribe.mailchimp import update_segments

class Command(BaseCommand):

    def handle(self, *args, **options):
        update_segments()
