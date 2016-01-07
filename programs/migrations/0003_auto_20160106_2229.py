# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0002_auto_20160106_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='name',
            field=models.CharField(help_text=b'Name of Program', max_length=100),
        ),
        migrations.AlterField(
            model_name='subprogram',
            name='name',
            field=models.CharField(help_text=b'Name of Program', max_length=100),
        ),
    ]
