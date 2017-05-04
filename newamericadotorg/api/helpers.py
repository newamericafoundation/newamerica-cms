from home.models import Post, HomePage
from programs.models import Program, Subprogram, AbstractContentPage
from home.models import Post
from issue.models import IssueOrTopic

def generate_image_url(image, filter_spec=None):
    if not filter_spec:
        return image.file.url

    signature = generate_signature(image.id, filter_spec)
    url = reverse('wagtailimages_serve', args=(signature, image.id, filter_spec))

    return url


def get_program_content_types(program_id):
    children = Page.objects.get(pk=program_id).get_children().type(AbstractContentPage)

    content_types = []
    for c in children:
        content_types.append({
            'id': c.id,
            'url': c.url,
            'slug': c.slug,
            'title': c.title
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
            program: p,
            projects: p.get_children().type(Subprogram).live().in_menu(),
            topics: p.get_children().type(IssueOrTopic).live().in_mene()
        })

    return { 'programs': program_data }

def content_types(request):
    '''
    For sitewide context_processor
    All available content_types
    '''
    content_classes = Post.__subclasses__()
    content_types = []
    for c in content_classes:
        content_types.append({
            'api_name': c._meta.model_name,
            'name': c._meta.verbose_name
        })

    return { 'content_types': content_types }
