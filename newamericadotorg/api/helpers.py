from home.models import Post, HomePage, CustomImage
from programs.models import Program, Subprogram, AbstractContentPage, PublicationsPage
from event.models import ProgramEventsPage, AllEventsHomePage
from issue.models import TopicHomePage
from person.models import ProgramPeoplePage
from issue.models import IssueOrTopic
from other_content.models import ProgramOtherPostsPage, OtherPostCategory
from policy_paper.models import ProgramPolicyPapersPage

from django.core.urlresolvers import reverse
from wagtail.images.views.serve import generate_signature
from wagtail.core.models import Page
from wagtail.images.models import SourceImageIOError

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


def get_content_type(obj):
    content_type = obj.get_ancestors().type(AbstractContentPage).first()
    if content_type:
        content_type = content_type.specific
        name = getattr(content_type, 'singular_title', None)
        name = obj.content_type.name if not name else name
        return {
            'id': content_type.id,
            'name': name,
            'title': content_type.title,
            'api_name': obj.content_type.model,
            'url': content_type.url,
            'slug': content_type.slug
            }
    name = getattr(obj, 'singular_title', None)
    name = obj.content_type.name if not name else name
    return {
        'id': obj.id,
        'name': name,
        'title': obj.content_type.name.title(),
        'api_name': obj.content_type.model,
        'url': obj.url,
        'slug': obj.slug
        }


def get_program_content_types(program):
    if isinstance(program, Program) or isinstance(program, Subprogram):
        page = program
    else:
        page = Page.objects.get(pk=program)

    children = page.get_children().type(AbstractContentPage).not_type(PublicationsPage).not_type(ProgramPeoplePage)\
        .not_type(TopicHomePage).not_type(ProgramEventsPage).not_type(AllEventsHomePage).not_type(ProgramPolicyPapersPage)\
        .live()

    content_types = []
    for c in children:
        c = c.specific
        name = getattr(c, 'singular_title', None)
        name = c.content_model._meta.verbose_name.title() if not name else name
        content_type = {
            'id': c.id,
            'url': c.url,
            'slug': c.slug,
            'title': c.title,
            'api_name': c.content_model.__name__.lower(),
            'name': name
        }
        if type(c) == ProgramOtherPostsPage:
            categories = c.get_children().type(OtherPostCategory).specific()
            cats = []
            for cat in categories:
                cats.append(cat.title)
            content_type['categories'] = cats
        content_types.append(content_type)

    return content_types

def get_subpages(page):
    children = page.get_children().not_type(AbstractContentPage).live()
    pages = []

    for c in children:
        pages.append({
            'id': c.id,
            'slug': c.slug,
            'url': c.url,
            'title': c.title,
            'search_description': c.search_description
        })

    return pages
