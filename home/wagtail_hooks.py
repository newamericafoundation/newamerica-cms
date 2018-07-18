from django.utils.safestring import mark_safe
from django.utils.html import format_html, format_html_join
from django.conf import settings
from wagtail.core import hooks
from wagtail.core.whitelist import attribute_rule, check_url, allow_without_attributes

@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    return {
        'blockquote': attribute_rule({'class': True}),
    }

@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        'js/hallo-custombuttons.js',
    ]
    js_includes = format_html_join('\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )
 
    return js_includes + format_html(
        """
        <script>
            registerHalloPlugin('blockquotebutton');
            registerHalloPlugin('blockquotebuttonwithclass');
        </script>
        """
    )

@hooks.register('insert_editor_css')
def editor_css():
    return format_html('<link rel="stylesheet" href="'+ settings.STATIC_URL + 'css/font-awesome.min.css" type="text/css">')
