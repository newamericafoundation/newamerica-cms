# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-04-25 06:35
from __future__ import unicode_literals

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0007_auto_20180414_0429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='acknowledgements',
            field=wagtail.fields.RichTextField(blank=True, null=True),
        ),
    ]
