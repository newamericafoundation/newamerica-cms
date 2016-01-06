# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_auto_20160104_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='rsvp_link',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]
