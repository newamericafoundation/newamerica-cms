# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-17 15:45
from __future__ import unicode_literals

from django.db import migrations
import wagtail.contrib.table_block.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20161020_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([('introduction', wagtail.wagtailcore.blocks.RichTextBlock()), ('heading', wagtail.wagtailcore.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('inline_image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(icon=b'image', required=True)), (b'align', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[(b'left', b'Left'), (b'right', b'Right'), (b'full-width', b'Full Width')])), (b'width', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[(b'initial', b'Auto'), (b'60%', b'60%'), (b'50%', b'50%'), (b'33.333%', b'33%'), (b'25%', b'25%')], default=b'initial'))], icon='image')), ('video', wagtail.wagtailembeds.blocks.EmbedBlock(icon='media')), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('button', wagtail.wagtailcore.blocks.StructBlock([(b'button_text', wagtail.wagtailcore.blocks.CharBlock(max_length=50, required=True)), (b'button_link', wagtail.wagtailcore.blocks.URLBlock(default=b'https://www.', required=True)), (b'alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[(b'left-aligned', b'Left'), (b'center-aligned', b'Center')]))])), ('iframe', wagtail.wagtailcore.blocks.StructBlock([(b'source_url', wagtail.wagtailcore.blocks.URLBlock(required=True)), (b'width', wagtail.wagtailcore.blocks.IntegerBlock(help_text=b'The maximum possible iframe width is 1050', max_value=1050)), (b'height', wagtail.wagtailcore.blocks.IntegerBlock())])), ('dataviz', wagtail.wagtailcore.blocks.StructBlock([(b'title', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'subheading', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'max_width', wagtail.wagtailcore.blocks.IntegerBlock()), (b'show_chart_buttons', wagtail.wagtailcore.blocks.BooleanBlock(default=False, required=False)), (b'container_id', wagtail.wagtailcore.blocks.CharBlock(required=True))])), ('google_map', wagtail.wagtailcore.blocks.StructBlock([(b'use_page_address', wagtail.wagtailcore.blocks.BooleanBlock(default=False, help_text=b'If selected, map will use the address already defined for this page, if applicable. For most posts besides events, this should be left unchecked and the form below should be completed.', required=False)), (b'street', wagtail.wagtailcore.blocks.TextBlock(required=False)), (b'city', wagtail.wagtailcore.blocks.TextBlock(default=b'Washington', required=False)), (b'state', wagtail.wagtailcore.blocks.TextBlock(default=b'D.C.', required=False)), (b'zipcode', wagtail.wagtailcore.blocks.TextBlock(default=b'200', required=False))])), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(help_text='Legacy option. Consider using Inline Image instead.', template='ui_elements/image_block.html'))]),
        ),
    ]
