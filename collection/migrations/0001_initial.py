# Generated by Django 3.0.11 on 2021-05-27 16:15

from django.db import migrations, models
import django.db.models.deletion
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0059_apply_collection_ordering'),
        ('home', '0057_auto_20210519_1133'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionsHomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Collections Homepage',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.StreamField([('introduction', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('heading', wagtail.core.blocks.CharBlock(form_classname='full title', icon='title', template='blocks/heading.html')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('inline_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=True)), ('align', wagtail.core.blocks.ChoiceBlock(choices=[('center', 'Centered'), ('left', 'Left'), ('right', 'Right')])), ('width', wagtail.core.blocks.ChoiceBlock(choices=[('initial', 'Auto'), ('width-133', 'Medium'), ('width-166', 'Large'), ('width-200', 'X-Large'), ('width-full', 'Full-width')])), ('use_original', wagtail.core.blocks.BooleanBlock(help_text='check if you do not want image compressed. Should be checked for all figures.', required=False)), ('figure_number', wagtail.core.blocks.CharBlock(max_length=3, required=False)), ('figure_title', wagtail.core.blocks.CharBlock(max_length=100, required=False)), ('open_image_on_click', wagtail.core.blocks.BooleanBlock(default=False, required=False))], icon='image')), ('video', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('table', wagtail.contrib.table_block.blocks.TableBlock(template='blocks/table.html')), ('button', wagtail.core.blocks.StructBlock([('button_text', wagtail.core.blocks.CharBlock(max_length=50, required=True)), ('button_link', wagtail.core.blocks.URLBlock(default='https://www.', required=True)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left-aligned', 'Left'), ('center-aligned', 'Center')]))])), ('iframe', wagtail.core.blocks.StructBlock([('source_url', wagtail.core.blocks.URLBlock(required=True)), ('column_width', wagtail.core.blocks.ChoiceBlock(choices=[('column-width', 'Column Width (max 650px)'), ('width-1200', 'Site Width (max 1200px)'), ('full-width', 'Full Width (max 100%)')], help_text='The maximum width of the iframe. Always use "Column Width" for non-report content types (e.g. blog posts, About pages). Never use "Full-Width" unless specifically instructed to by your designer.', required=False)), ('width', wagtail.core.blocks.IntegerBlock(help_text='The iframe will look best if the width is at least as large as the column width. Note that the maximum, in 2018 and earlier, used to be 1050.', required=True)), ('height', wagtail.core.blocks.IntegerBlock(required=True)), ('fallback_image', wagtail.images.blocks.ImageChooserBlock(help_text='The fallback image will be rendered for the PDF', icon='image', required=False)), ('fallback_image_align', wagtail.core.blocks.ChoiceBlock(choices=[('center', 'Centered'), ('left', 'Left'), ('right', 'Right')])), ('fallback_image_width', wagtail.core.blocks.ChoiceBlock(choices=[('initial', 'Auto'), ('width-133', 'Medium'), ('width-166', 'Large'), ('width-200', 'X-Large')])), ('fallback_image_use_original', wagtail.core.blocks.BooleanBlock(help_text='check if you do not want image compressed. Should be checked for all figures.', required=False))], icon='link')), ('datawrapper', wagtail.core.blocks.StructBlock([('chart_id', wagtail.core.blocks.CharBlock(help_text='The 5 character ID for the chart, e.g. "kT4Qi"', required=True)), ('embed_code', wagtail.core.blocks.TextBlock(help_text='The "Responsive Embed" code provided by Datawrapper', required=True)), ('width', wagtail.core.blocks.ChoiceBlock(choices=[('column-width', 'Column Width (max 650px)'), ('width-1200', 'Site Width (max 1200px)'), ('full-width', 'Full Width (max 100%)')], help_text='The maximum width of the chart. Always use "Column Width" for non-report content types (e.g. blog posts, About pages). Never use "Full-Width" unless specifically instructed to by your designer.', required=False)), ('fallback_image', wagtail.images.blocks.ImageChooserBlock(help_text='The fallback image will be rendered for the PDF', icon='image', required=False)), ('fallback_image_align', wagtail.core.blocks.ChoiceBlock(choices=[('center', 'Centered'), ('left', 'Left'), ('right', 'Right')])), ('fallback_image_width', wagtail.core.blocks.ChoiceBlock(choices=[('initial', 'Auto'), ('width-133', 'Medium'), ('width-166', 'Large'), ('width-200', 'X-Large')]))], icon='code')), ('dataviz', wagtail.core.blocks.StructBlock([('container_id', wagtail.core.blocks.CharBlock(required=True)), ('width', wagtail.core.blocks.ChoiceBlock(choices=[('column-width', 'Column Width (max 650px)'), ('width-1200', 'Site Width (max 1200px)'), ('full-width', 'Full Width (max 100%)')], required=False)), ('title', wagtail.core.blocks.CharBlock(required=False)), ('subheading', wagtail.core.blocks.RichTextBlock(required=False)), ('max_width', wagtail.core.blocks.IntegerBlock(help_text='for legacy dataviz projects', required=False)), ('show_chart_buttons', wagtail.core.blocks.BooleanBlock(default=False, required=False))], icon='code')), ('timeline', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('subheading', wagtail.core.blocks.CharBlock(required=False)), ('default_view', wagtail.core.blocks.ChoiceBlock(choices=[('timeline', 'Timeline'), ('list', 'List')], help_text='Should the default view be a timeline or a list?', required=False)), ('major_timeline_splits', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('start_date', wagtail.core.blocks.DateBlock(required=True)), ('end_date', wagtail.core.blocks.DateBlock(required=False)), ('date_display_type', wagtail.core.blocks.ChoiceBlock(choices=[('year', 'Year'), ('month', 'Month'), ('day', 'Day')], help_text='Controls how specific the date is displayed'))]), default='', required=False)), ('event_eras', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('start_date', wagtail.core.blocks.DateBlock(required=True)), ('end_date', wagtail.core.blocks.DateBlock(required=False)), ('date_display_type', wagtail.core.blocks.ChoiceBlock(choices=[('year', 'Year'), ('month', 'Month'), ('day', 'Day')], help_text='Controls how specific the date is displayed'))]), default='', required=False)), ('event_categories', wagtail.core.blocks.ListBlock(wagtail.core.blocks.CharBlock(), default='', required=False)), ('event_list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('italicize_title', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('category', wagtail.core.blocks.CharBlock(required=False)), ('start_date', wagtail.core.blocks.DateBlock(required=True)), ('end_date', wagtail.core.blocks.DateBlock(required=False)), ('date_display_type', wagtail.core.blocks.ChoiceBlock(choices=[('year', 'Year'), ('month', 'Month'), ('day', 'Day')], help_text='Controls how specific the date is displayed'))])))], icon='arrows-up-down')), ('google_map', wagtail.core.blocks.StructBlock([('use_page_address', wagtail.core.blocks.BooleanBlock(default=False, help_text='If selected, map will use the address already defined for this page, if applicable. For most posts besides events, this should be left unchecked and the form below should be completed.', required=False)), ('street', wagtail.core.blocks.TextBlock(required=False)), ('city', wagtail.core.blocks.TextBlock(default='Washington', required=False)), ('state', wagtail.core.blocks.TextBlock(default='D.C.', required=False)), ('zipcode', wagtail.core.blocks.TextBlock(default='200', required=False))], icon='site')), ('resource_kit', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('description', wagtail.core.blocks.TextBlock(required=False)), ('resources', wagtail.core.blocks.StreamBlock([('post', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('resource', wagtail.core.blocks.PageChooserBlock(required=True))], icon='redirect', label='Post')), ('external_resource', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('resource', wagtail.core.blocks.URLBlock(required=True))], icon='site', label='External resource')), ('attachment', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('resource', wagtail.documents.blocks.DocumentChooserBlock(required=True))], icon='doc-full', label='Attachment'))]))], icon='folder')), ('people', wagtail.core.blocks.StreamBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('description', wagtail.core.blocks.TextBlock(required=False)), ('person', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.TextBlock(required=True)), ('title', wagtail.core.blocks.TextBlock(help_text='125 character limit', max_length=125, required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=False)), ('twitter', wagtail.core.blocks.URLBlock(required=False))]))], help_text='Grid of people with short bios that appear on click', icon='group')), ('panels', wagtail.core.blocks.StreamBlock([('panel', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.TextBlock()), ('body', wagtail.core.blocks.StreamBlock([('introduction', wagtail.core.blocks.RichTextBlock(icon='openquote')), ('heading', wagtail.core.blocks.CharBlock(form_classname='full title', icon='title', template='blocks/heading.html')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('inline_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=True)), ('align', wagtail.core.blocks.ChoiceBlock(choices=[('center', 'Centered'), ('left', 'Left'), ('right', 'Right')])), ('width', wagtail.core.blocks.ChoiceBlock(choices=[('initial', 'Auto'), ('width-133', 'Medium'), ('width-166', 'Large'), ('width-200', 'X-Large'), ('width-full', 'Full-width')])), ('use_original', wagtail.core.blocks.BooleanBlock(help_text='check if you do not want image compressed. Should be checked for all figures.', required=False)), ('figure_number', wagtail.core.blocks.CharBlock(max_length=3, required=False)), ('figure_title', wagtail.core.blocks.CharBlock(max_length=100, required=False)), ('open_image_on_click', wagtail.core.blocks.BooleanBlock(default=False, required=False))], icon='image')), ('video', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('table', wagtail.contrib.table_block.blocks.TableBlock(template='blocks/table.html')), ('button', wagtail.core.blocks.StructBlock([('button_text', wagtail.core.blocks.CharBlock(max_length=50, required=True)), ('button_link', wagtail.core.blocks.URLBlock(default='https://www.', required=True)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left-aligned', 'Left'), ('center-aligned', 'Center')]))])), ('iframe', wagtail.core.blocks.StructBlock([('source_url', wagtail.core.blocks.URLBlock(required=True)), ('column_width', wagtail.core.blocks.ChoiceBlock(choices=[('column-width', 'Column Width (max 650px)'), ('width-1200', 'Site Width (max 1200px)'), ('full-width', 'Full Width (max 100%)')], help_text='The maximum width of the iframe. Always use "Column Width" for non-report content types (e.g. blog posts, About pages). Never use "Full-Width" unless specifically instructed to by your designer.', required=False)), ('width', wagtail.core.blocks.IntegerBlock(help_text='The iframe will look best if the width is at least as large as the column width. Note that the maximum, in 2018 and earlier, used to be 1050.', required=True)), ('height', wagtail.core.blocks.IntegerBlock(required=True)), ('fallback_image', wagtail.images.blocks.ImageChooserBlock(help_text='The fallback image will be rendered for the PDF', icon='image', required=False)), ('fallback_image_align', wagtail.core.blocks.ChoiceBlock(choices=[('center', 'Centered'), ('left', 'Left'), ('right', 'Right')])), ('fallback_image_width', wagtail.core.blocks.ChoiceBlock(choices=[('initial', 'Auto'), ('width-133', 'Medium'), ('width-166', 'Large'), ('width-200', 'X-Large')])), ('fallback_image_use_original', wagtail.core.blocks.BooleanBlock(help_text='check if you do not want image compressed. Should be checked for all figures.', required=False))], icon='link')), ('datawrapper', wagtail.core.blocks.StructBlock([('chart_id', wagtail.core.blocks.CharBlock(help_text='The 5 character ID for the chart, e.g. "kT4Qi"', required=True)), ('embed_code', wagtail.core.blocks.TextBlock(help_text='The "Responsive Embed" code provided by Datawrapper', required=True)), ('width', wagtail.core.blocks.ChoiceBlock(choices=[('column-width', 'Column Width (max 650px)'), ('width-1200', 'Site Width (max 1200px)'), ('full-width', 'Full Width (max 100%)')], help_text='The maximum width of the chart. Always use "Column Width" for non-report content types (e.g. blog posts, About pages). Never use "Full-Width" unless specifically instructed to by your designer.', required=False)), ('fallback_image', wagtail.images.blocks.ImageChooserBlock(help_text='The fallback image will be rendered for the PDF', icon='image', required=False)), ('fallback_image_align', wagtail.core.blocks.ChoiceBlock(choices=[('center', 'Centered'), ('left', 'Left'), ('right', 'Right')])), ('fallback_image_width', wagtail.core.blocks.ChoiceBlock(choices=[('initial', 'Auto'), ('width-133', 'Medium'), ('width-166', 'Large'), ('width-200', 'X-Large')]))], icon='code')), ('dataviz', wagtail.core.blocks.StructBlock([('container_id', wagtail.core.blocks.CharBlock(required=True)), ('width', wagtail.core.blocks.ChoiceBlock(choices=[('column-width', 'Column Width (max 650px)'), ('width-1200', 'Site Width (max 1200px)'), ('full-width', 'Full Width (max 100%)')], required=False)), ('title', wagtail.core.blocks.CharBlock(required=False)), ('subheading', wagtail.core.blocks.RichTextBlock(required=False)), ('max_width', wagtail.core.blocks.IntegerBlock(help_text='for legacy dataviz projects', required=False)), ('show_chart_buttons', wagtail.core.blocks.BooleanBlock(default=False, required=False))], icon='code')), ('timeline', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('subheading', wagtail.core.blocks.CharBlock(required=False)), ('default_view', wagtail.core.blocks.ChoiceBlock(choices=[('timeline', 'Timeline'), ('list', 'List')], help_text='Should the default view be a timeline or a list?', required=False)), ('major_timeline_splits', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('start_date', wagtail.core.blocks.DateBlock(required=True)), ('end_date', wagtail.core.blocks.DateBlock(required=False)), ('date_display_type', wagtail.core.blocks.ChoiceBlock(choices=[('year', 'Year'), ('month', 'Month'), ('day', 'Day')], help_text='Controls how specific the date is displayed'))]), default='', required=False)), ('event_eras', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('start_date', wagtail.core.blocks.DateBlock(required=True)), ('end_date', wagtail.core.blocks.DateBlock(required=False)), ('date_display_type', wagtail.core.blocks.ChoiceBlock(choices=[('year', 'Year'), ('month', 'Month'), ('day', 'Day')], help_text='Controls how specific the date is displayed'))]), default='', required=False)), ('event_categories', wagtail.core.blocks.ListBlock(wagtail.core.blocks.CharBlock(), default='', required=False)), ('event_list', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('italicize_title', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('category', wagtail.core.blocks.CharBlock(required=False)), ('start_date', wagtail.core.blocks.DateBlock(required=True)), ('end_date', wagtail.core.blocks.DateBlock(required=False)), ('date_display_type', wagtail.core.blocks.ChoiceBlock(choices=[('year', 'Year'), ('month', 'Month'), ('day', 'Day')], help_text='Controls how specific the date is displayed'))])))], icon='arrows-up-down')), ('google_map', wagtail.core.blocks.StructBlock([('use_page_address', wagtail.core.blocks.BooleanBlock(default=False, help_text='If selected, map will use the address already defined for this page, if applicable. For most posts besides events, this should be left unchecked and the form below should be completed.', required=False)), ('street', wagtail.core.blocks.TextBlock(required=False)), ('city', wagtail.core.blocks.TextBlock(default='Washington', required=False)), ('state', wagtail.core.blocks.TextBlock(default='D.C.', required=False)), ('zipcode', wagtail.core.blocks.TextBlock(default='200', required=False))], icon='site')), ('resource_kit', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=True)), ('description', wagtail.core.blocks.TextBlock(required=False)), ('resources', wagtail.core.blocks.StreamBlock([('post', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('resource', wagtail.core.blocks.PageChooserBlock(required=True))], icon='redirect', label='Post')), ('external_resource', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('resource', wagtail.core.blocks.URLBlock(required=True))], icon='site', label='External resource')), ('attachment', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('resource', wagtail.documents.blocks.DocumentChooserBlock(required=True))], icon='doc-full', label='Attachment'))]))], icon='folder'))]))], icon='doc-empty-inverse'))], icon='list-ul')), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='Legacy option. Consider using Inline Image instead.', icon='placeholder', template='blocks/image_block.html'))], blank=True, null=True)),
                ('story_excerpt', models.CharField(blank=True, max_length=500, null=True)),
                ('custom_interface', models.BooleanField(default=False)),
                ('data_project_external_script', models.CharField(blank=True, help_text='Specify the name of the external script file within the na-data-projects/projects AWS directory to include that script in the body of the document.', max_length=140, null=True)),
                ('subheading', models.TextField(blank=True, null=True)),
                ('programs_description', wagtail.core.fields.RichTextField(blank=True)),
                ('programs_list', wagtail.core.fields.StreamField([('program', wagtail.core.blocks.StructBlock([('page', wagtail.core.blocks.PageChooserBlock(page_type=['programs.Program'], required=True)), ('description', wagtail.core.blocks.RichTextBlock(required=False))], icon='doc-empty', label='Program'))], blank=True)),
                ('resources_description', wagtail.core.fields.RichTextField(blank=True)),
                ('resources_list', wagtail.core.fields.StreamField([('external_resource', wagtail.core.blocks.StructBlock([('link', wagtail.core.blocks.URLBlock(required=True)), ('title', wagtail.core.blocks.CharBlock(required=True)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=False))], icon='link-external', label='External resource')), ('attachment', wagtail.core.blocks.StructBlock([('document', wagtail.documents.blocks.DocumentChooserBlock(required=True)), ('title', wagtail.core.blocks.CharBlock(required=True)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=False))], icon='doc-full', label='Attachment'))], blank=True)),
                ('people_description', wagtail.core.fields.RichTextField(blank=True)),
                ('people_list', wagtail.core.fields.StreamField([('person', wagtail.core.blocks.PageChooserBlock(icon='user', label='Person', page_type=['person.Person']))], blank=True)),
                ('publications_description', wagtail.core.fields.RichTextField(blank=True)),
                ('publications_list', wagtail.core.fields.StreamField([('publication', wagtail.core.blocks.StructBlock([('page', wagtail.core.blocks.PageChooserBlock(page_type=['home.Post'], required=True)), ('title', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=False))], icon='doc-empty', label='Publication'))], blank=True)),
                ('events_description', wagtail.core.fields.RichTextField(blank=True)),
                ('events_list', wagtail.core.fields.StreamField([('event', wagtail.core.blocks.StructBlock([('page', wagtail.core.blocks.PageChooserBlock(page_type=['event.Event'], required=True)), ('title', wagtail.core.blocks.CharBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image', required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False))], icon='date', label='Event'))], blank=True)),
                ('story_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.CustomImage')),
            ],
            options={
                'verbose_name': 'Collection',
            },
            bases=('wagtailcore.page',),
        ),
    ]