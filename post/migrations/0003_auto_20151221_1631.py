# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20151221_0056'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='book_home_page',
            new_name='BookHomePage',
        ),
    ]
