# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quoted', '0002_auto_20160108_2102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quoted',
            name='summary',
        ),
        migrations.AlterField(
            model_name='quoted',
            name='source',
            field=models.TextField(max_length=8000),
        ),
    ]
