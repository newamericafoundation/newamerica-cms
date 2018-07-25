# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-17 15:45
from __future__ import unicode_literals

from django.db import migrations
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20161020_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=wagtail.core.fields.StreamField([('introduction', wagtail.core.blocks.RichTextBlock()), ('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('inline_image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock(icon=b'image', required=True)), (b'align', wagtail.core.blocks.ChoiceBlock(choices=[(b'left', b'Left'), (b'right', b'Right'), (b'full-width', b'Full Width')])), (b'width', wagtail.core.blocks.ChoiceBlock(choices=[(b'initial', b'Auto'), (b'60%', b'60%'), (b'50%', b'50%'), (b'33.333%', b'33%'), (b'25%', b'25%')], default=b'initial'))], icon='image')), ('video', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('button', wagtail.core.blocks.StructBlock([(b'button_text', wagtail.core.blocks.CharBlock(max_length=50, required=True)), (b'button_link', wagtail.core.blocks.URLBlock(default=b'https://www.', required=True)), (b'alignment', wagtail.core.blocks.ChoiceBlock(choices=[(b'left-aligned', b'Left'), (b'center-aligned', b'Center')]))])), ('iframe', wagtail.core.blocks.StructBlock([(b'source_url', wagtail.core.blocks.URLBlock(required=True)), (b'width', wagtail.core.blocks.IntegerBlock(help_text=b'The maximum possible iframe width is 1050', max_value=1050)), (b'height', wagtail.core.blocks.IntegerBlock())])), ('dataviz', wagtail.core.blocks.StructBlock([(b'title', wagtail.core.blocks.CharBlock(required=False)), (b'subheading', wagtail.core.blocks.RichTextBlock(required=False)), (b'max_width', wagtail.core.blocks.IntegerBlock()), (b'show_chart_buttons', wagtail.core.blocks.BooleanBlock(default=False, required=False)), (b'container_id', wagtail.core.blocks.CharBlock(required=True))])), ('google_map', wagtail.core.blocks.StructBlock([(b'use_page_address', wagtail.core.blocks.BooleanBlock(default=False, help_text=b'If selected, map will use the address already defined for this page, if applicable. For most posts besides events, this should be left unchecked and the form below should be completed.', required=False)), (b'street', wagtail.core.blocks.TextBlock(required=False)), (b'city', wagtail.core.blocks.TextBlock(default=b'Washington', required=False)), (b'state', wagtail.core.blocks.TextBlock(default=b'D.C.', required=False)), (b'zipcode', wagtail.core.blocks.TextBlock(default=b'200', required=False))])), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='Legacy option. Consider using Inline Image instead.', template='components/image_block.html'))]),
        ),
    ]
