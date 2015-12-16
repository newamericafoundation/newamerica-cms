# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programsubprogramrelationship',
            name='subprogram',
            field=models.ForeignKey(to='programs.Subprogram', related_name='+'),
        ),
    ]
