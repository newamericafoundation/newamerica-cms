from home.models import Post, HomePage
from programs.models import Program, Subprogram, AbstractContentPage
from home.models import Post
from issue.models import IssueOrTopic

from django.core.urlresolvers import reverse
from wagtail.wagtailimages.views.serve import generate_signature
from wagtail.wagtailcore.models import Page

newamericadotorg_content_types = [
    { 'name': 'Blog Post', 'api_name': 'blogpost', 'slug': 'blogs'  },
    { 'name': 'Policy Paper', 'api_name': 'policypaper', 'slug': 'policy-papers'  },
    { 'name': 'Book', 'api_name': 'book', 'slug': 'books'  },
    { 'name': 'In Depth Project', 'api_name': 'indepthproject', 'slug': 'in-depth'  },
    { 'name': 'In the News', 'api_name': 'quoted', 'slug': 'in-the-news'  },
    { 'name': 'Press Release', 'api_name': 'pressrelease', 'slug': 'press-releases'  },
    { 'name': 'Article', 'api_name': 'article', 'slug': 'articles' },
    { 'name': 'Podcast', 'api_name': 'podcast', 'slug': 'podcasts' },
]


programpage_contenttype_map = {
    'programblogpostspage': newamericadotorg_content_types[0],
    'programpolicypaperspage': newamericadotorg_content_types[1],
    'programbookspage': newamericadotorg_content_types[2],
    'programquotedpage': newamericadotorg_content_types[4],
    'programpressreleasespage': newamericadotorg_content_types[5],
    'programarticlespage': newamericadotorg_content_types[6],
    'programpodcastspage': newamericadotorg_content_types[7],
}

def generate_image_url(image, filter_spec=None):
    if not filter_spec:
        return image.file.url

    signature = generate_signature(image.id, filter_spec)
    url = reverse('wagtailimages_serve', args=(signature, image.id, filter_spec))

    return url


def get_program_content_types(program):
    if isinstance(program, Program) or isinstance(program, Subprogram):
        page = program
    else:
        page = Page.objects.get(pk=program)

    children = page.get_children().type(AbstractContentPage)

    content_types = []
    for c in children:
        content_types.append({
            'id': c.id,
            'url': c.url,
            'slug': c.slug,
            'title': c.title,
            'api_name': programpage_contenttype_map[c.content_type.model]['api_name'],
            'name': programpage_contenttype_map[c.content_type.model]['name']
        })

    return content_types

def get_subpages(page):
    children = page.get_children().not_type(AbstractContentPage)
    pages = []

    for c in children:
        pages.append({
            'id': c.id,
            'slug': c.slug,
            'url': c.url,
            'title': c.title
        })

    return pages

def program_data(request):
    '''
    For sitewide context_processor
    Programs and related projects or topics
    '''
    program_data = []
    programs = Program.objects.in_menu().order_by("title").exclude(location=True)
    for p in programs:
        program_data.append({
            'program': p,
            'projects': p.get_children().type(Subprogram).live().in_menu(),
            'topics': p.get_children().type(IssueOrTopic).live().in_menu()
        })

    return { 'program_data': program_data }

def content_types(request):
    '''
    For sitewide context_processor
    All available content_types
    '''
    # content_classes = Post.__subclasses__()
    # content_types = []
    # for c in content_classes:
    #     content_types.append({
    #         'api_name': c._meta.model_name,
    #         'name': c._meta.verbose_name
    #     })

    return { 'content_types': newamericadotorg_content_types }
