# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0003_auto_20151221_0134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ourpeoplepage',
            options={'verbose_name': 'Homepage for all People in NAF'},
        ),
        migrations.AlterModelOptions(
            name='programpeoplepage',
            options={'verbose_name': 'Our People Page for Programs'},
        ),
    ]
