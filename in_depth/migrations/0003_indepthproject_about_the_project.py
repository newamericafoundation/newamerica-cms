# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-30 21:42
from __future__ import unicode_literals

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('in_depth', '0002_indepthproject_project_logo_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='indepthproject',
            name='about_the_project',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
    ]
