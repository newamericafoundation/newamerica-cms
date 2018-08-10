from django.core.management.base import BaseCommand
from wagtail.core.models import Page
from programs.models import Program, Subprogram, FeaturedProgramPage, FeaturedSubprogramPage
from home.models import ProgramAboutPage, ProgramAboutHomePage, Page
from wagtail.contrib.redirects.models import Redirect

class Command(BaseCommand):
    def handle(self, *args, **options):
        ProgramAboutHomePage.objects.all().delete()
        programs = Program.objects.all()
        subprograms = Subprogram.objects.all()

        remove_new_program_about_pages(self, programs)
        remove_new_program_about_pages(self, subprograms, False)

def remove_new_program_about_pages(self, programs, with_sidebar=True):
    for p in programs:
        if not p.about_us_page:
            continue

        a = p.about_us_page.specific
        a.slug = a.slug.replace('_legacy', '')
        a.save()
        a.save_revision().publish()

        self.stdout.write('changed %s and published' % a.url)
