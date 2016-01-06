# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_allblogpostpages_programbloghome'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='programbloghome',
            options={'verbose_name': 'Blog Homepage for Program'},
        ),
    ]
