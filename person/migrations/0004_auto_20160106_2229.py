# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0003_auto_20160106_2128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='bio',
        ),
        migrations.AddField(
            model_name='person',
            name='long_bio',
            field=models.TextField(max_length=5000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='short_bio',
            field=models.TextField(max_length=1000, null=True),
        ),
    ]
