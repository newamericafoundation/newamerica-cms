# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0003_auto_20151215_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='role',
            field=models.CharField(max_length=100, choices=[(b'Board Member', b'Board Member'), (b'Staff', b'Staff'), (b'Fellow', b'Fellow'), (b'Program Fellow', b'Program Fellow')]),
        ),
    ]
