# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-18 15:46
from __future__ import unicode_literals

from django.db import migrations
import wagtail.core.fields
import wagtail.documents.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('other_content', '0004_auto_20180718_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otherpost',
            name='attachment',
            field=wagtail.core.fields.StreamField((('attachment', wagtail.documents.blocks.DocumentChooserBlock(required=False)),), blank=True, null=True),
        ),
    ]
