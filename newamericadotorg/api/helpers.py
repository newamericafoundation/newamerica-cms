def get_content_types(parent_model):
    root_pages = parent_model.clean_subpage_models()

    content_types = []

    for model in root_pages:
        page = model.objects.first()
        if page:
            if getattr(page, 'related_content_type', None):
                content = page.related_content_type._meta
                content_types.append({
                    'api_name': content.model_name,
                    'name': content.verbose_name,
                    'plural_name': content.verbose_name_plural,
                    'slug': page.slug
                })

    return content_types
