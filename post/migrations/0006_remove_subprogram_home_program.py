# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20151211_2045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subprogram',
            name='home_program',
        ),
    ]
