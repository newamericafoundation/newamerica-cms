# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-03-03 06:06
from __future__ import unicode_literals

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0007_auto_20180718_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='alleventshomepage',
            name='body',
            field=wagtail.fields.RichTextField(blank=True),
        ),
    ]
