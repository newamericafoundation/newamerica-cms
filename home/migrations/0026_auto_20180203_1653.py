# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-02-03 21:53
from __future__ import unicode_literals

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_auto_20180201_1451'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orgsimplepage',
            options={'verbose_name': 'New America Post'},
        ),
        migrations.AlterModelOptions(
            name='programsimplepage',
            options={'verbose_name': 'Post'},
        ),
        migrations.AddField(
            model_name='orgsimplepage',
            name='page_description',
            field=wagtail.fields.RichTextField(blank=True),
        ),
    ]
