# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-09-18 16:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0010_auto_20170712_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='partner_heading',
            field=models.TextField(default=b'Sponsors & Partners'),
        ),
    ]
