from django.db import models

from post.models import Post

from wagtail.wagtailcore.models import Page



class Event(Post):
    """
    Event class that inherits from the abstract Post
    model and creates pages for Events.
    """
    pass

class EventsHomePage(Page):
    parent_page_types = ['home.HomePage',]
    subpage_types = []

    def get_context(self, request):
        context = super(EventsHomePage, self).get_context(request)

        context['events'] = Event.objects.all()
        return context

    class Meta:
        verbose_name = "Homepage for all Events"