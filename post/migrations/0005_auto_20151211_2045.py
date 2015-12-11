# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20151211_2031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subprogram',
            name='home_program',
        ),
        migrations.AddField(
            model_name='subprogram',
            name='home_program',
            field=models.ManyToManyField(to='post.Program'),
        ),
    ]
