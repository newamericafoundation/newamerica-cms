from django.db import models

from home.models import Post

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel

from programs.models import Program

from django.utils import timezone
from django.utils.timezone import now

from mysite.pagination import paginate_results


class Event(Post):
    """
    Event class that inherits from the abstract Post
    model and creates pages for Events.
    """
    parent_page_types = ['ProgramEventsPage']
    subpage_types = []

    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now, blank=True, null=True)
    host_organization = models.TextField(default='New America', blank=True, null=True)
    street_address = models.TextField(default='740 15th St NW #900')
    city = models.TextField(default='Washington')
    state = models.TextField(default='D.C.')
    zipcode = models.TextField(default='20005')
    rsvp_link = models.URLField(default='http://www.')

    content_panels = Post.content_panels + [
        FieldPanel('end_date'),
        FieldPanel('start_time'),
        FieldPanel('end_time'),
        FieldPanel('rsvp_link'),
        FieldPanel('host_organization'),
        FieldPanel('street_address'),
        FieldPanel('city'),
        FieldPanel('state'),
        FieldPanel('zipcode'),
    ]


class AllEventsHomePage(Page):
    """
    Page which inherits from abstract Page model and returns every
    Event in the Event model for the Events homepage
    """
    parent_page_types = ['home.HomePage',]
    subpage_types = ['Event']

    def get_context(self, request):
        context = super(AllEventsHomePage, self).get_context(request)

        all_posts = Event.objects.all().order_by("-date")
        context['all_posts'] = paginate_results(request, all_posts)

        return context

    class Meta:
        verbose_name = "Homepage for all Events"


class ProgramEventsPage(Page):
    """
    Page which inherits from abstract Page model and returns every
    Event associated with a specific Program which is determined
    using the url path
    """
    parent_page_types = ['programs.Program',]
    subpage_types = ['Event']

    def get_context(self, request):
        context = super(ProgramEventsPage, self).get_context(request)
        program_slug = request.path.split("/")[-3]
        program = Program.objects.get(slug=program_slug)
        
        all_posts = Event.objects.filter(parent_programs=program).order_by("-date")
        context['all_posts'] = paginate_results(request, all_posts)
        
        context['program'] = program
        return context

    class Meta:
        verbose_name = "Events Homepage for Program"

