# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_person_program'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='role',
            field=models.CharField(max_length=50, choices=[('Board Member', 'Board Member'), ('Staff', 'Staff'), ('New America Fellow', 'New America Fellow'), ('Program Fellow', 'Program Fellow')]),
        ),
    ]
