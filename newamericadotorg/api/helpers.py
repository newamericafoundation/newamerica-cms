from home.models import Post, HomePage, CustomImage
from programs.models import Program, Subprogram, AbstractContentPage, PublicationsPage
from event.models import ProgramEventsPage, AllEventsHomePage
from issue.models import TopicHomePage
from person.models import ProgramPeoplePage
from issue.models import IssueOrTopic

from django.core.urlresolvers import reverse
from wagtail.wagtailimages.views.serve import generate_signature
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.models import SourceImageIOError

# eventually hard encode these values into respective the ContentTypePage model
newamericadotorg_content_types = [
    { 'name': 'Blog Post', 'api_name': 'blogpost', 'slug': 'blogs', 'title': 'Blogs'  },
    { 'name': 'Policy Paper', 'api_name': 'policypaper', 'slug': 'policy-papers', 'title': 'Policy Papers'  },
    { 'name': 'Book', 'api_name': 'book', 'slug': 'books', 'title': 'Books'  },
    { 'name': 'In Depth Project', 'api_name': 'indepthproject', 'slug': 'in-depth', 'title': 'In Depth Projects'  },
    { 'name': 'In the News Piece', 'api_name': 'quoted', 'slug': 'in-the-news', 'title': 'In the News'  },
    { 'name': 'Press Release', 'api_name': 'pressrelease', 'slug': 'press-releases', 'title': 'Press Releases'  },
    { 'name': 'Article/Op-Ed', 'api_name': 'article', 'slug': 'articles', 'title': 'Articles and Op-Eds' },
    { 'name': 'Podcast', 'api_name': 'podcast', 'slug': 'podcasts', 'title': 'Podcasts' },
    { 'name': 'Weekly Article', 'api_name': 'weeklyarticle', 'slug': 'weekly-articles', 'title': 'Weekly Articles' },
    { 'name': 'Other', 'api_name': 'customcontenttype', 'slug': 'other', 'title': 'Other'},
    { 'name': 'Report', 'api_name': 'report', 'slug': 'reports', 'title': 'Reports' }
]


programpage_contenttype_map = {
    'programblogpostspage': newamericadotorg_content_types[0],
    'programpolicypaperspage': newamericadotorg_content_types[1],
    'programbookspage': newamericadotorg_content_types[2],
    'programquotedpage': newamericadotorg_content_types[4],
    'programpressreleasespage': newamericadotorg_content_types[5],
    'programarticlespage': newamericadotorg_content_types[6],
    'programpodcastspage': newamericadotorg_content_types[7],
    'programcustomcontenttypepage': newamericadotorg_content_types[8],
    'reportshomepage': newamericadotorg_content_types[9]
}

def generate_image_rendition(image, filter_spec=None):
    if not image:
        return None
    if not filter_spec:
        return image.file
    #return None;
    img = CustomImage.objects.get(pk=image.id);
    if not image:
        return image.file
    try:
        rendition = img.get_rendition(filter_spec)
        # signature = generate_signature(image.id, filter_spec)
        # url = reverse('wagtailimages_serve', args=(signature, image.id, filter_spec))
        return rendition
    except SourceImageIOError:
        return None

def generate_image_url(image, filter_spec=None):
    img = generate_image_rendition(image, filter_spec)
    if not img:
        return None

    return img.url


def get_content_type(api_name):
    for c in newamericadotorg_content_types:
        if c['api_name'] == api_name:
            return c;

    if api_name == 'person':
        return { 'name': 'Person', 'api_name': 'person', 'slug': 'our-people', 'title': 'People'  }

    if api_name == 'event':
        return { 'name': 'Event', 'api_name': 'event', 'slug': 'events', 'title': 'Events'  }

    if(getattr(programpage_contenttype_map, api_name, None)):
        return programpage_contenttype_map[api_name]

    return { 'name': 'Homepage', 'api_name': api_name, 'slug': None, 'title': 'Homepages' }


def get_program_content_types(program):
    if isinstance(program, Program) or isinstance(program, Subprogram):
        page = program
    else:
        page = Page.objects.get(pk=program)

    children = page.get_children().type(AbstractContentPage).not_type(PublicationsPage).not_type(ProgramPeoplePage)\
        .not_type(TopicHomePage).not_type(ProgramEventsPage).not_type(AllEventsHomePage)

    content_types = []
    for c in children:
        content_type = {
            'id': c.id,
            'url': c.url,
            'slug': c.slug,
            'title': c.title,
            'api_name': programpage_contenttype_map[c.content_type.model]['api_name'],
            'name': programpage_contenttype_map[c.content_type.model]['name'],
            'categories': [] # for custom content types
        }
        if c.content_type.model == 'programcustomcontenttypepage':
            for cat in c.get_children():
                content_type['categories'].append({
                    'name': cat.title,
                    'id': cat.id,
                    'slug': cat.slug
                })
        content_types.append(content_type)

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
