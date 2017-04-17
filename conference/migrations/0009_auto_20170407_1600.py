# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-07 20:00
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0008_auto_20170320_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='hotel_city',
            field=models.TextField(blank=True, default=b'Washington', null=True),
        ),
        migrations.AddField(
            model_name='conference',
            name='hotel_details',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='conference',
            name='hotel_location_name',
            field=models.TextField(blank=True, help_text=b'Name of building (e.g. the Kennedy Center)', null=True),
        ),
        migrations.AddField(
            model_name='conference',
            name='hotel_state',
            field=models.TextField(blank=True, default=b'D.C.', null=True),
        ),
        migrations.AddField(
            model_name='conference',
            name='hotel_street',
            field=models.TextField(blank=True, default=b'740 15th St NW #900', null=True),
        ),
        migrations.AddField(
            model_name='conference',
            name='hotel_zipcode',
            field=models.TextField(blank=True, default=b'20005', null=True),
        ),
        migrations.AddField(
            model_name='conference',
            name='venue_details',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True, null=True),
        ),
    ]
