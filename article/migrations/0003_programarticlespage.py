# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
        ('article', '0002_auto_20151222_2116'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramArticlesPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Articles Homepage for Program',
            },
            bases=('wagtailcore.page',),
        ),
    ]
