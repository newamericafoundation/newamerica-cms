from home.models import Post

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel

from mysite.helpers import paginate_results, get_posts_and_programs


class Podcast(Post):
    """
    Podcast class that inherits from the abstract Post
    model and creates pages for Podcasts.
    """
    parent_page_types = ['ProgramPodcastsPage']
    subpage_types = []

    soundcloud = StreamField([
        ('soundcloud_embed', EmbedBlock()),
    ])

    content_panels = Post.content_panels + [
        StreamFieldPanel('soundcloud'),

    ]


class AllPodcastsHomePage(Page):
    """
    A page which inherits from the abstract Page model
    and returns every Podcast in the Podcast model for
    the organization wide Podcast homepage
    """

    parent_page_types = ['home.HomePage']
    subpage_types = []

    def get_context(self, request):
        context = super(AllPodcastsHomePage, self).get_context(request)
        all_posts = Podcast.objects.all().order_by("-date")

        context['all_posts'] = paginate_results(request, all_posts)

        return context

    class Meta:
        verbose_name = "Homepage for all Podcasts"


class ProgramPodcastsPage(Page):
    """
    A page which inherits from the abstract Page model and
    returns all Podcasts associated with a sepcific program
    or Subprogram
    """

    parent_page_types = ['programs.Program', 'programs.Subprogram']
    subpage_types = ['Podcast']

    def get_context(self, request):
        return get_posts_and_programs(
            self,
            request,
            ProgramPodcastsPage,
            Podcast
        )

    class Meta:
        verbose_name = "Podcast Homepage for Program and Subprograms"
