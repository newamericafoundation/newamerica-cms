from django.utils.safestring import mark_safe
from django.utils.html import format_html, format_html_join
from django.conf import settings

from wagtail.admin.rich_text.editors.draftail import features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler, BlockElementHandler
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
    return format_html('<style>{}</style>', '''
        .Draftail-block--blockquote {
            color: rgba(0,0,0,0.4);
            border-left: 1px solid #ccc;
            margin-left: 10px;
            padding-left: 40px;
        }

        .Draftail-block--header-four,
        .Draftail-block--header-five {
            font-weight: bold
        }

        .Draftail-block--pullquote{
            padding-top: 25px;
            padding-bottom: 25px;
            padding-left: 40px;
            padding-right: 40px;
            margin-left: 0;
            margin-right: 0;
            border-top: 1px solid #333;
            border-bottom: 1px solid #333;
            font-weight: bold;
            font-size: 1.1em;
        }
    ''')
    return format_html('<link rel="stylesheet" href="'+ settings.STATIC_URL + 'css/font-awesome.min.css" type="text/css">')


@hooks.register('register_rich_text_features')
def register_pullquote_feature(features):
    """
    Registering the `blockquote` feature, which uses the `blockquote` Draft.js block type,
    and is stored as HTML with a `<blockquote>` tag.
    """
    feature_name = 'pullquote'
    type_ = 'pullquote'
    tag = 'blockquote'

    control = {
        'type': type_,
        'icon': 'icon icon-openquote',
        'description': 'Pullquote',
        'element': 'blockquote'
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control)
    )

    features.default_features.append(feature_name)
    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'blockquote[class="pullquote"]': BlockElementHandler(type_)},
        'to_database_format': {
            'block_map': {
                type_: {
                    'element': tag,
                    'props': {
                        'class': 'pullquote'
                    }
                }
            }
        },
    })


@hooks.register('register_rich_text_features')
def register_blockquote_feature(features):
    """
    Registering the `blockquote` feature, which uses the `blockquote` Draft.js block type,
    and is stored as HTML with a `<blockquote>` tag.
    """
    feature_name = 'na-blockquote'
    type_ = 'blockquote'
    tag = 'blockquote'

    control = {
        'type': type_,
        'icon': 'icon icon-arrow-right',
        'description': 'Blockquote',
        'element': 'blockquote',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control)
    )

    features.default_features.append(feature_name)

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {tag: BlockElementHandler(type_)},
        'to_database_format': {'block_map': {type_: tag}},
    })
