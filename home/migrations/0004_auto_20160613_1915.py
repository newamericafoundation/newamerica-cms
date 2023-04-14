# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-13 19:15
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.contrib.table_block.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.embeds.blocks
import wagtail.images.blocks
import wagtail.images.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_redirectpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customrendition',
            name='file',
            field=models.ImageField(height_field='height', upload_to=wagtail.images.models.get_rendition_upload_to, width_field='width'),
        ),
        migrations.AlterField(
            model_name='orgsimplepage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('video', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('button', wagtail.blocks.StructBlock([(b'button_text', wagtail.blocks.CharBlock(max_length=50, required=True)), (b'button_link', wagtail.blocks.URLBlock(default=b'https://www.', required=True)), (b'alignment', wagtail.blocks.ChoiceBlock(choices=[(b'left-aligned', b'Left'), (b'center-aligned', b'Center')]))]))]),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('video', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('button', wagtail.blocks.StructBlock([(b'button_text', wagtail.blocks.CharBlock(max_length=50, required=True)), (b'button_link', wagtail.blocks.URLBlock(default=b'https://www.', required=True)), (b'alignment', wagtail.blocks.ChoiceBlock(choices=[(b'left-aligned', b'Left'), (b'center-aligned', b'Center')]))]))]),
        ),
        migrations.AlterField(
            model_name='programsimplepage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('video', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('button', wagtail.blocks.StructBlock([(b'button_text', wagtail.blocks.CharBlock(max_length=50, required=True)), (b'button_link', wagtail.blocks.URLBlock(default=b'https://www.', required=True)), (b'alignment', wagtail.blocks.ChoiceBlock(choices=[(b'left-aligned', b'Left'), (b'center-aligned', b'Center')]))]))]),
        ),
    ]
