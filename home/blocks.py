from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtaildocs.blocks import DocumentChooserBlock

from wagtail.wagtaildocs.models import Document
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel,MultiFieldPanel, \
	InlinePanel, PageChooserPanel, StreamFieldPanel

from django.utils.html import format_html, format_html_join
from django.conf import settings
from wagtail.wagtailcore import hooks

@hooks.register('insert_editor_js')
def editor_js():
	js_files = [
		'../static/dataviz/js/modaltest.js',
		'../static/dataviz/js/data-visualization-customizer.js',
	]
	js_includes = format_html_join('\n', '<script src="{0}{1}"></script>',
		((settings.STATIC_URL, filename) for filename in js_files)
	)
	return js_includes + format_html(
		"""
		<div id="data-visualization-customizer-app"></div>
		<script>

		  console.log('hello!!');
		  
		</script>
		"""
	)

class MapBlock(blocks.StructBlock):
	title = blocks.CharBlock(required=True)
	short_description = blocks.TextBlock(required=False)
	# data_file = DocumentChooserBlock()
	data_url = blocks.CharBlock(required=True)
	variable_option = blocks.CharBlock(required=True)
 
	class Meta:
		template = './home/map.html'
		icon = 'cogs'
		label = 'Map'