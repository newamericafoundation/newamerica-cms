# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-24 22:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('in_depth', '0007_auto_20161020_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='indepthproject',
            name='show_data_download_links',
            field=models.BooleanField(default=True),
        ),
    ]
