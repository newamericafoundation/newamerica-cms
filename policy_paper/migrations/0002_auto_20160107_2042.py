# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('policy_paper', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='policypaper',
            old_name='url',
            new_name='paper_url',
        ),
    ]
