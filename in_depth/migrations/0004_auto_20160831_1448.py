# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-31 18:48
from __future__ import unicode_literals

from django.db import migrations
import home.blocks
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('in_depth', '0003_indepthproject_about_the_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indepthsection',
            name='panels',
            field=wagtail.core.fields.StreamField([('panel', wagtail.core.blocks.StructBlock([('panel_title', wagtail.core.blocks.CharBlock(required=True)), ('panel_color_theme', wagtail.core.blocks.ChoiceBlock(choices=[('white', 'White'), ('grey', 'Grey'), ('black', 'Black')])), ('panel_body', wagtail.core.blocks.StreamBlock([(b'heading', wagtail.core.blocks.CharBlock(classname='full title')), (b'paragraph', wagtail.core.blocks.RichTextBlock()), (b'image', wagtail.images.blocks.ImageChooserBlock(icon='image')), (b'video', wagtail.embeds.blocks.EmbedBlock(icon='media')), (b'table', wagtail.contrib.table_block.blocks.TableBlock()), (b'button', wagtail.core.blocks.StructBlock([(b'button_text', wagtail.core.blocks.CharBlock(max_length=50, required=True)), (b'button_link', wagtail.core.blocks.URLBlock(default=b'https://www.', required=True)), (b'alignment', wagtail.core.blocks.ChoiceBlock(choices=[(b'left-aligned', b'Left'), (b'center-aligned', b'Center')]))])), (b'iframe', wagtail.core.blocks.StructBlock([(b'source_url', wagtail.core.blocks.URLBlock(required=True)), (b'width', home.blocks.IntegerBlock(help_text=b'The maximum possible iframe width is 1050', max_value=1050)), (b'height', home.blocks.IntegerBlock())])), (b'dataviz', wagtail.core.blocks.StructBlock([(b'title', wagtail.core.blocks.CharBlock()), (b'subheading', wagtail.core.blocks.RichTextBlock()), (b'max_width', home.blocks.IntegerBlock()), (b'container_id', wagtail.core.blocks.CharBlock(required=True))]))]))]))], blank=True, null=True),
        ),
    ]
