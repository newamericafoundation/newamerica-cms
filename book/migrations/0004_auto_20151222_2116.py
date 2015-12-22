# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_programbookspage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='programbookspage',
            options={'verbose_name': 'Books Homepage for Program'},
        ),
    ]
