# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-18 15:00
from __future__ import unicode_literals

from django.db import migrations
import wagtail.fields
import wagtail.documents.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('press_release', '0003_auto_20180327_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pressrelease',
            name='attachment',
            field=wagtail.fields.StreamField((('attachment', wagtail.documents.blocks.DocumentChooserBlock(null=True, required=False)),)),
        ),
    ]
