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
                ('page_ptr', models.OneToOneField(serialize=False, to='wagtailcore.Page', primary_key=True, parent_link=True, auto_created=True)),
                ('name', models.CharField(max_length=150)),
                ('bio', models.CharField(max_length=1000)),
                ('role', models.CharField(choices=[('Board Member', 'Board Member'), ('Staff', 'Staff'), ('Fellow', 'Fellow'), ('Program Fellow', 'Program Fellow')], max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
