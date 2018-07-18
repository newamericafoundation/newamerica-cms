# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-28 16:00
from __future__ import unicode_literals

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0002_conference_invitation_only'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='speakers',
            field=wagtail.core.fields.StreamField([(b'person', wagtail.core.blocks.StructBlock([(b'name', wagtail.core.blocks.TextBlock(required=True)), (b'title', wagtail.core.blocks.TextBlock()), (b'description', wagtail.core.blocks.RichTextBlock()), (b'image', wagtail.images.blocks.ImageChooserBlock(icon=b'image', required=False)), (b'twitter', wagtail.core.blocks.URLBlock(required=False))]))], blank=True, null=True),
        ),
    ]
