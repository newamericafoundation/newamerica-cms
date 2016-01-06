# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20151223_1858'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AllBlogPostPages',
            new_name='AllBlogPostsHomePage',
        ),
        migrations.RenameModel(
            old_name='ProgramBlogHome',
            new_name='ProgramBlogPostsPage',
        ),
    ]
