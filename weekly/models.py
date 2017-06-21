from __future__ import unicode_literals

from home.models import Post

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.blocks import PageChooserBlock

from newamericadotorg.helpers import paginate_results


class Weekly(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['WeeklyEdition']

    def get_context(self, request):
        context = super(Weekly, self).get_context(request)

        all_posts = WeeklyEdition.objects.all().live().order_by('-first_published_at')

        context['all_posts'] = paginate_results(request, all_posts)
        context['latest_edition'] = int(all_posts.first().title.split(' ')[1])
        return context

    class Meta:
        verbose_name = "Homepage for all Weekly Editions"


class WeeklyEdition(Page):
    parent_page_types = ['Weekly']
    subpage_types = ['WeeklyArticle']

    def get_context(self, request):
        context = super(WeeklyEdition, self).get_context(request)
        all_posts = WeeklyEdition.objects.all().live().order_by('-first_published_at')

        context['latest_edition'] = all_posts.first().title.split(' ')[1]
        return context



class WeeklyArticle(Post):
    parent_page_types = ['WeeklyEdition']
    subpage_types = []

    def get_context(self, request):
        context = super(WeeklyArticle, self).get_context(request)

        context['siblings'] = self.get_siblings(inclusive=True)
        all_posts = WeeklyEdition.objects.all().live().order_by('-first_published_at')
        context['latest_edition'] = all_posts.first().title.split(' ')[1]

        return context

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Weekly Article'
