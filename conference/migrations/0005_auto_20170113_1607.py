# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-13 21:07
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0004_auto_20161207_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='speakers',
            field=wagtail.wagtailcore.fields.StreamField([(b'person', wagtail.wagtailcore.blocks.StructBlock([(b'name', wagtail.wagtailcore.blocks.TextBlock(required=True)), (b'title', wagtail.wagtailcore.blocks.TextBlock(help_text=b'125 character limit', max_length=125, required=False)), (b'description', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(icon=b'image', required=False)), (b'twitter', wagtail.wagtailcore.blocks.URLBlock(required=False))]))], blank=True, null=True),
        ),
    ]