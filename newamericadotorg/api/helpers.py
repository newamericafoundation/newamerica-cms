from home.models import Post

def get_content_types():
    subposts = Post.__subclasses__()
    content_types = []

    for model in subposts:
        content = model._meta
        content_types.append({
            'api_name': content.model_name,
            'name': content.verbose_name
        })

    return content_types

def generate_image_url(image, filter_spec=None):
    if not filter_spec:
        return image.file.url

    signature = generate_signature(image.id, filter_spec)
    url = reverse('wagtailimages_serve', args=(signature, image.id, filter_spec))

    return url
