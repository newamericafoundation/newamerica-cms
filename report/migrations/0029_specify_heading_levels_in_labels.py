# Generated by Django 3.2.18 on 2024-02-16 16:52

import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0028_optional_boxblock_title_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='sections',
            field=wagtail.fields.StreamField([('section', wagtail.blocks.StructBlock([('title', wagtail.blocks.TextBlock(label='Title (Heading 1)')), ('hide_title', wagtail.blocks.BooleanBlock(required=False)), ('body', wagtail.blocks.StreamBlock([('introduction', wagtail.blocks.RichTextBlock(icon='openquote')), ('heading', wagtail.blocks.CharBlock(form_classname='full title', icon='title', label='Heading (Heading 2)', template='blocks/heading.html')), ('paragraph', wagtail.blocks.RichTextBlock()), ('inline_image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=True)), ('align', wagtail.blocks.ChoiceBlock(choices=[('center', 'Centered'), ('left', 'Left'), ('right', 'Right')])), ('width', wagtail.blocks.ChoiceBlock(choices=[('initial', 'Auto'), ('width-133', 'Medium'), ('width-166', 'Large'), ('width-200', 'X-Large'), ('width-full', 'Full-width')])), ('use_original', wagtail.blocks.BooleanBlock(help_text='check if you do not want image compressed. Should be checked for all figures.', required=False)), ('figure_number', wagtail.blocks.CharBlock(max_length=3, required=False)), ('figure_title', wagtail.blocks.CharBlock(max_length=100, required=False)), ('open_image_on_click', wagtail.blocks.BooleanBlock(default=False, required=False)), ('alt_text', wagtail.blocks.CharBlock(help_text='A concise description of the image for users of assistive technology.', required=False, verbose_name='Alternative text'))], icon='image')), ('video', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('table', wagtail.contrib.table_block.blocks.TableBlock(template='blocks/table.html')), ('button', wagtail.blocks.StructBlock([('button_text', wagtail.blocks.CharBlock(max_length=50, required=True)), ('button_link', wagtail.blocks.URLBlock(default='https://www.', required=True)), ('alignment', wagtail.blocks.ChoiceBlock(choices=[('left-aligned', 'Left'), ('center-aligned', 'Center')]))])), ('iframe', wagtail.blocks.StructBlock([('source_url', wagtail.blocks.URLBlock(required=True)), ('column_width', wagtail.blocks.ChoiceBlock(choices=[('column-width', 'Column Width (max 650px)'), ('width-1200', 'Site Width (max 1200px)'), ('full-width', 'Full Width (max 100%)')], help_text='The maximum width of the iframe. Always use "Column Width" for non-report content types (e.g. blog posts, About pages). Never use "Full-Width" unless specifically instructed to by your designer.', required=False)), ('fixed_height', wagtail.blocks.BooleanBlock(help_text='Leave unchecked if you want width-to-height ratio to be preserved on smaller screens. Check to ignore the width value and instead use the full width of the column, with a fixed height.', required=False)), ('width', wagtail.blocks.IntegerBlock(help_text='The iframe will look best if the width is at least as large as the column width. Note that the maximum, in 2018 and earlier, used to be 1050.', required=True)), ('height', wagtail.blocks.IntegerBlock(required=True)), ('fallback_image', wagtail.images.blocks.ImageChooserBlock(help_text='The fallback image will be rendered for the PDF', icon='image', required=False)), ('fallback_image_align', wagtail.blocks.ChoiceBlock(choices=[('center', 'Centered'), ('left', 'Left'), ('right', 'Right')])), ('fallback_image_width', wagtail.blocks.ChoiceBlock(choices=[('initial', 'Auto'), ('width-133', 'Medium'), ('width-166', 'Large'), ('width-200', 'X-Large')])), ('fallback_image_use_original', wagtail.blocks.BooleanBlock(help_text='check if you do not want image compressed. Should be checked for all figures.', required=False)), ('fallback_image_alt_text', wagtail.blocks.CharBlock(help_text='A concise description of the image for users of assistive technology.', required=False, verbose_name='Fallback image alternative text'))], icon='link')), ('datawrapper', wagtail.blocks.StructBlock([('chart_id', wagtail.blocks.CharBlock(help_text='The 5 character ID for the chart, e.g. "kT4Qi"', required=True)), ('embed_code', wagtail.blocks.TextBlock(help_text='The "Responsive Embed" code provided by Datawrapper', required=True)), ('width', wagtail.blocks.ChoiceBlock(choices=[('column-width', 'Column Width (max 650px)'), ('width-1200', 'Site Width (max 1200px)'), ('full-width', 'Full Width (max 100%)')], help_text='The maximum width of the chart. Always use "Column Width" for non-report content types (e.g. blog posts, About pages). Never use "Full-Width" unless specifically instructed to by your designer.', required=False)), ('fallback_image', wagtail.images.blocks.ImageChooserBlock(help_text='The fallback image will be rendered for the PDF', icon='image', required=False)), ('fallback_image_align', wagtail.blocks.ChoiceBlock(choices=[('center', 'Centered'), ('left', 'Left'), ('right', 'Right')])), ('fallback_image_width', wagtail.blocks.ChoiceBlock(choices=[('initial', 'Auto'), ('width-133', 'Medium'), ('width-166', 'Large'), ('width-200', 'X-Large')])), ('fallback_image_alt_text', wagtail.blocks.CharBlock(help_text='A concise description of the image for users of assistive technology.', required=False, verbose_name='Fallback image alternative text'))], icon='code')), ('dataviz', wagtail.blocks.StructBlock([('container_id', wagtail.blocks.CharBlock(required=True)), ('width', wagtail.blocks.ChoiceBlock(choices=[('column-width', 'Column Width (max 650px)'), ('width-1200', 'Site Width (max 1200px)'), ('full-width', 'Full Width (max 100%)')], required=False)), ('title', wagtail.blocks.CharBlock(required=False)), ('subheading', wagtail.blocks.RichTextBlock(required=False)), ('max_width', wagtail.blocks.IntegerBlock(help_text='for legacy dataviz projects', required=False)), ('show_chart_buttons', wagtail.blocks.BooleanBlock(default=False, required=False)), ('static_image_fallback', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=False)), ('align', wagtail.blocks.ChoiceBlock(choices=[('center', 'Centered'), ('left', 'Left'), ('right', 'Right')], required=False)), ('width', wagtail.blocks.ChoiceBlock(choices=[('initial', 'Auto'), ('width-133', 'Medium'), ('width-166', 'Large'), ('width-200', 'X-Large')], required=False)), ('use_original', wagtail.blocks.BooleanBlock(help_text='check if you do not want image compressed. Should be checked for all figures.', required=False)), ('figure_number', wagtail.blocks.CharBlock(max_length=3, required=False)), ('figure_title', wagtail.blocks.CharBlock(max_length=100, required=False)), ('open_image_on_click', wagtail.blocks.BooleanBlock(default=False, required=False)), ('alt_text', wagtail.blocks.CharBlock(help_text='A concise description of the image for users of assistive technology.', required=False, verbose_name='Alternative text'))], icon='image'))], icon='code')), ('timeline', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=True)), ('subheading', wagtail.blocks.CharBlock(required=False)), ('default_view', wagtail.blocks.ChoiceBlock(choices=[('timeline', 'Timeline'), ('list', 'List')], help_text='Should the default view be a timeline or a list?', required=False)), ('major_timeline_splits', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=True)), ('start_date', wagtail.blocks.DateBlock(required=True)), ('end_date', wagtail.blocks.DateBlock(required=False)), ('date_display_type', wagtail.blocks.ChoiceBlock(choices=[('year', 'Year'), ('month', 'Month'), ('day', 'Day')], help_text='Controls how specific the date is displayed'))]), default='', required=False)), ('event_eras', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=True)), ('start_date', wagtail.blocks.DateBlock(required=True)), ('end_date', wagtail.blocks.DateBlock(required=False)), ('date_display_type', wagtail.blocks.ChoiceBlock(choices=[('year', 'Year'), ('month', 'Month'), ('day', 'Day')], help_text='Controls how specific the date is displayed'))]), default='', required=False)), ('event_categories', wagtail.blocks.ListBlock(wagtail.blocks.CharBlock(), default='', required=False)), ('event_list', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=True)), ('italicize_title', wagtail.blocks.BooleanBlock(default=False, required=False)), ('description', wagtail.blocks.RichTextBlock(required=False)), ('category', wagtail.blocks.CharBlock(required=False)), ('start_date', wagtail.blocks.DateBlock(required=True)), ('end_date', wagtail.blocks.DateBlock(required=False)), ('date_display_type', wagtail.blocks.ChoiceBlock(choices=[('year', 'Year'), ('month', 'Month'), ('day', 'Day')], help_text='Controls how specific the date is displayed'))])))], icon='arrows-up-down')), ('google_map', wagtail.blocks.StructBlock([('use_page_address', wagtail.blocks.BooleanBlock(default=False, help_text='If selected, map will use the address already defined for this page, if applicable. For most posts besides events, this should be left unchecked and the form below should be completed.', required=False)), ('street', wagtail.blocks.TextBlock(required=False)), ('city', wagtail.blocks.TextBlock(default='Washington', required=False)), ('state', wagtail.blocks.TextBlock(default='D.C.', required=False)), ('zipcode', wagtail.blocks.TextBlock(default='200', required=False))], icon='site')), ('resource_kit', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=True)), ('description', wagtail.blocks.TextBlock(required=False)), ('resources', wagtail.blocks.StreamBlock([('post', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=False)), ('image_alt_text', wagtail.blocks.CharBlock(required=False)), ('description', wagtail.blocks.RichTextBlock(required=False)), ('resource', wagtail.blocks.PageChooserBlock(required=True))], icon='redirect', label='Post')), ('external_resource', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=False)), ('image_alt_text', wagtail.blocks.CharBlock(required=False)), ('description', wagtail.blocks.RichTextBlock(required=False)), ('resource', wagtail.blocks.URLBlock(required=True))], icon='site', label='External resource')), ('attachment', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=False)), ('image_alt_text', wagtail.blocks.CharBlock(required=False)), ('description', wagtail.blocks.RichTextBlock(required=False)), ('resource', wagtail.documents.blocks.DocumentChooserBlock(required=True))], icon='doc-full', label='Attachment'))]))], icon='folder')), ('box', wagtail.blocks.StructBlock([('title', wagtail.blocks.TextBlock(required=False)), ('body', wagtail.blocks.StreamBlock([('paragraph', wagtail.blocks.RichTextBlock()), ('inline_image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=True)), ('align', wagtail.blocks.ChoiceBlock(choices=[('center', 'Centered'), ('left', 'Left'), ('right', 'Right')])), ('width', wagtail.blocks.ChoiceBlock(choices=[('initial', 'Auto'), ('width-133', 'Medium'), ('width-166', 'Large'), ('width-200', 'X-Large'), ('width-full', 'Full-width')])), ('use_original', wagtail.blocks.BooleanBlock(help_text='check if you do not want image compressed. Should be checked for all figures.', required=False)), ('figure_number', wagtail.blocks.CharBlock(max_length=3, required=False)), ('figure_title', wagtail.blocks.CharBlock(max_length=100, required=False)), ('open_image_on_click', wagtail.blocks.BooleanBlock(default=False, required=False)), ('alt_text', wagtail.blocks.CharBlock(help_text='A concise description of the image for users of assistive technology.', required=False, verbose_name='Alternative text'))], icon='image')), ('video', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('iframe', wagtail.blocks.StructBlock([('source_url', wagtail.blocks.URLBlock(required=True)), ('column_width', wagtail.blocks.ChoiceBlock(choices=[('column-width', 'Column Width (max 650px)'), ('width-1200', 'Site Width (max 1200px)'), ('full-width', 'Full Width (max 100%)')], help_text='The maximum width of the iframe. Always use "Column Width" for non-report content types (e.g. blog posts, About pages). Never use "Full-Width" unless specifically instructed to by your designer.', required=False)), ('fixed_height', wagtail.blocks.BooleanBlock(help_text='Leave unchecked if you want width-to-height ratio to be preserved on smaller screens. Check to ignore the width value and instead use the full width of the column, with a fixed height.', required=False)), ('width', wagtail.blocks.IntegerBlock(help_text='The iframe will look best if the width is at least as large as the column width. Note that the maximum, in 2018 and earlier, used to be 1050.', required=True)), ('height', wagtail.blocks.IntegerBlock(required=True)), ('fallback_image', wagtail.images.blocks.ImageChooserBlock(help_text='The fallback image will be rendered for the PDF', icon='image', required=False)), ('fallback_image_align', wagtail.blocks.ChoiceBlock(choices=[('center', 'Centered'), ('left', 'Left'), ('right', 'Right')])), ('fallback_image_width', wagtail.blocks.ChoiceBlock(choices=[('initial', 'Auto'), ('width-133', 'Medium'), ('width-166', 'Large'), ('width-200', 'X-Large')])), ('fallback_image_use_original', wagtail.blocks.BooleanBlock(help_text='check if you do not want image compressed. Should be checked for all figures.', required=False)), ('fallback_image_alt_text', wagtail.blocks.CharBlock(help_text='A concise description of the image for users of assistive technology.', required=False, verbose_name='Fallback image alternative text'))], icon='link')), ('datawrapper', wagtail.blocks.StructBlock([('chart_id', wagtail.blocks.CharBlock(help_text='The 5 character ID for the chart, e.g. "kT4Qi"', required=True)), ('embed_code', wagtail.blocks.TextBlock(help_text='The "Responsive Embed" code provided by Datawrapper', required=True)), ('width', wagtail.blocks.ChoiceBlock(choices=[('column-width', 'Column Width (max 650px)'), ('width-1200', 'Site Width (max 1200px)'), ('full-width', 'Full Width (max 100%)')], help_text='The maximum width of the chart. Always use "Column Width" for non-report content types (e.g. blog posts, About pages). Never use "Full-Width" unless specifically instructed to by your designer.', required=False)), ('fallback_image', wagtail.images.blocks.ImageChooserBlock(help_text='The fallback image will be rendered for the PDF', icon='image', required=False)), ('fallback_image_align', wagtail.blocks.ChoiceBlock(choices=[('center', 'Centered'), ('left', 'Left'), ('right', 'Right')])), ('fallback_image_width', wagtail.blocks.ChoiceBlock(choices=[('initial', 'Auto'), ('width-133', 'Medium'), ('width-166', 'Large'), ('width-200', 'X-Large')])), ('fallback_image_alt_text', wagtail.blocks.CharBlock(help_text='A concise description of the image for users of assistive technology.', required=False, verbose_name='Fallback image alternative text'))], icon='code')), ('dataviz', wagtail.blocks.StructBlock([('container_id', wagtail.blocks.CharBlock(required=True)), ('width', wagtail.blocks.ChoiceBlock(choices=[('column-width', 'Column Width (max 650px)'), ('width-1200', 'Site Width (max 1200px)'), ('full-width', 'Full Width (max 100%)')], required=False)), ('title', wagtail.blocks.CharBlock(required=False)), ('subheading', wagtail.blocks.RichTextBlock(required=False)), ('max_width', wagtail.blocks.IntegerBlock(help_text='for legacy dataviz projects', required=False)), ('show_chart_buttons', wagtail.blocks.BooleanBlock(default=False, required=False)), ('static_image_fallback', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=False)), ('align', wagtail.blocks.ChoiceBlock(choices=[('center', 'Centered'), ('left', 'Left'), ('right', 'Right')], required=False)), ('width', wagtail.blocks.ChoiceBlock(choices=[('initial', 'Auto'), ('width-133', 'Medium'), ('width-166', 'Large'), ('width-200', 'X-Large')], required=False)), ('use_original', wagtail.blocks.BooleanBlock(help_text='check if you do not want image compressed. Should be checked for all figures.', required=False)), ('figure_number', wagtail.blocks.CharBlock(max_length=3, required=False)), ('figure_title', wagtail.blocks.CharBlock(max_length=100, required=False)), ('open_image_on_click', wagtail.blocks.BooleanBlock(default=False, required=False)), ('alt_text', wagtail.blocks.CharBlock(help_text='A concise description of the image for users of assistive technology.', required=False, verbose_name='Alternative text'))], icon='image'))], icon='code'))]))]))]))], required=False, template='components/report_section_body.html'))], blank=True, null=True, use_json_field=True),
        ),
    ]
