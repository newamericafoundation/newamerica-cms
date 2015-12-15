# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_auto_20151215_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='role',
            field=models.CharField(max_length=100, choices=[(b'BM', b'Board Member'), (b'S', b'Staff'), (b'F', b'Fellow'), (b'PF', b'Program Fellow')]),
        ),
    ]
