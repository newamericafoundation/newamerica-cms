# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-14 14:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20160627_2120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='recent_carousel',
        ),
    ]
