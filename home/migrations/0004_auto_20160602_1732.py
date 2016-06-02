# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 17:32
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.contrib.table_block.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks
import wagtail.wagtailimages.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_redirectpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customrendition',
            name='file',
            field=models.ImageField(height_field='height', upload_to=wagtail.wagtailimages.models.get_rendition_upload_to, width_field='width'),
        ),
        migrations.AlterField(
            model_name='orgsimplepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([('heading', wagtail.wagtailcore.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(icon='image')), ('video', wagtail.wagtailembeds.blocks.EmbedBlock(icon='media')), ('table', wagtail.contrib.table_block.blocks.TableBlock())]),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([('heading', wagtail.wagtailcore.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(icon='image')), ('video', wagtail.wagtailembeds.blocks.EmbedBlock(icon='media')), ('table', wagtail.contrib.table_block.blocks.TableBlock())]),
        ),
        migrations.AlterField(
            model_name='programsimplepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([('heading', wagtail.wagtailcore.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(icon='image')), ('video', wagtail.wagtailembeds.blocks.EmbedBlock(icon='media')), ('table', wagtail.contrib.table_block.blocks.TableBlock())]),
        ),
    ]
