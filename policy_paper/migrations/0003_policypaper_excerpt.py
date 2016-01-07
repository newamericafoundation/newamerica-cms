# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('policy_paper', '0002_auto_20160107_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='policypaper',
            name='excerpt',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
