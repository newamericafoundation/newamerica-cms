from django.conf import settings
from django.http import HttpResponseForbidden
from django.urls import include, path, reverse
from django.utils.html import format_html, format_html_join
from wagtail import hooks
from wagtail.admin.menu import AdminOnlyMenuItem, Menu, SubmenuMenuItem
from wagtail.admin.rich_text.converters.html_to_contentstate import BlockElementHandler
from wagtail.admin.rich_text.editors.draftail import features as draftail_features
from wagtail.whitelist import attribute_rule

from .views import clear_cache_view


@hooks.register("register_admin_urls")
def register_command_urls():
    return [
        path(
            "clear_cache/",
            include(
                (
                    [
                        path(
                            "",
                            clear_cache_view,
                            name="clear",
                        )
                    ],
                    "cache",
                ),
                namespace="cache",
            ),
        )
    ]


@hooks.register("register_admin_menu_item")
def register_commands_menu_item():
    sync_menu_item = AdminOnlyMenuItem(
        "Sync Campaign Monitor",
        reverse("campaign_monitor:sync"),
        classnames="icon icon-mail",
        order=10,
    )
    clear_cache_menu_item = AdminOnlyMenuItem(
        "Clear Cache",
        reverse("cache:clear"),
        classnames="icon icon-placeholder",
        order=20,
    )
    submenu = Menu(
        items=[
            sync_menu_item,
            clear_cache_menu_item,
        ],
    )
    return SubmenuMenuItem("Commands", submenu, icon_name="code", order=10000)


@hooks.register('construct_page_listing_buttons')
def remove_copy_button_for_non_superusers(buttons, page, page_perms, context=None):
    if not page_perms.user.is_superuser:
        for top_button in buttons:
            if hasattr(top_button, 'dropdown_buttons'):
                top_button.dropdown_buttons = [
                    # 20 = the priority value of the "Copy" button, as
                    # defined in wagtail
                    b for b in top_button.dropdown_buttons if b.priority != 20
                ]


@hooks.register('before_copy_page')
def before_copy_page(request, page):
    # Permit copying pages only for superusers
    if not request.user.is_superuser:
        return HttpResponseForbidden()


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


@hooks.register('insert_global_admin_css')
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
        'icon': 'openquote',
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
        'icon': 'arrow-right',
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
