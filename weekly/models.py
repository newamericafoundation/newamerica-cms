from __future__ import unicode_literals

from django.db import models

from home.models import Post

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel

from mysite.pagination import paginate_results

class Weekly(Page):
    parent_page_types = ['home.HomePage',]
    subpage_types = ['WeeklyEdition']

    def get_context(self, request):
        context = super(Weekly, self).get_context(request)

        all_posts = WeeklyEdition.objects.all()

        context['all_posts'] = paginate_results(request, all_posts)

        return context

    class Meta:
        verbose_name = "Homepage for all Weekly Editions"


class WeeklyEdition(Page):
    parent_page_types = ['Weekly',]
    subpage_types = ['WeeklyArticle']

    def get_context(self, request):
        context = super(WeeklyEdition, self).get_context(request)
        
        all_posts = self.get_children()
        
        context['all_posts'] = paginate_results(request, all_posts)
        
        return context


class WeeklyArticle(Post):
    parent_page_types = ['WeeklyEdition']
    subpage_types = []

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

