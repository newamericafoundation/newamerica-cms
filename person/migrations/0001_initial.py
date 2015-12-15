# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0001_initial'),
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('name', models.CharField(max_length=150)),
                ('bio', models.TextField(max_length=1000)),
                ('role', models.CharField(max_length=100, choices=[(b'BR', b'Board Member'), (b'S', b'Staff'), (b'F', b'Fellow'), (b'PF', b'Program Fellow')])),
                ('program', models.ForeignKey(blank=True, to='programs.Program', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
