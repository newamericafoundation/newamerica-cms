# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='podcast',
            old_name='soundcloud_embed',
            new_name='soundcloud',
        ),
    ]
