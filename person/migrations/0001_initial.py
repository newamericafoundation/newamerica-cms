# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, parent_link=True, to='wagtailcore.Page', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=150)),
                ('bio', models.CharField(max_length=1000)),
                ('role', models.CharField(choices=[('Board Member', 'Board Member'), ('Staff', 'Staff'), ('New America Fellow', 'New America Fellow'), ('Program Fellow', 'Program Fellow')], max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
