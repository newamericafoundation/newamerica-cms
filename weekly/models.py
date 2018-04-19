from __future__ import unicode_literals

from home.models import Post

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.blocks import PageChooserBlock

from programs.models import AbstractContentPage
from newamericadotorg.helpers import paginate_results
from home.models import AbstractHomeContentPage

class Weekly(AbstractContentPage):
    parent_page_types = ['home.HomePage']
    subpage_types = ['WeeklyEdition']

    def get_context(self, request):
        context = super(Weekly, self).get_context(request)

        all_posts = WeeklyEdition.objects.all().live().public().order_by('-first_published_at')

        context['all_posts'] = paginate_results(request, all_posts)
        context['latest_edition'] = all_posts.first()
        return context

    class Meta:
        verbose_name = "Weekly Editions"


class WeeklyEdition(Page):
    parent_page_types = ['Weekly']
    subpage_types = ['WeeklyArticle']

class WeeklyArticle(Post):
    parent_page_types = ['WeeklyEdition']
    subpage_types = []

    def get_context(self, request):
        context = super(WeeklyArticle, self).get_context(request)
        context['edition'] = self.get_parent()
        return context

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Weekly Article'

class AllWeeklyArticlesHomePage(AbstractHomeContentPage):
    parent_page_types = ['home.HomePage']
    subpage_types = []

    @property
    def content_model(self):
        return WeeklyArticle
