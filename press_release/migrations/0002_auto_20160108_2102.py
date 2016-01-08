# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('press_release', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pressrelease',
            name='sub_headline',
            field=models.TextField(null=True, blank=True),
        ),
    ]
