# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
        ('quoted', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllQuotedHomePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Homepage for all Quoted Pieces (formerly In The News)',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ProgramQuotedPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Quoted Homepage for Programs (formerly In The News)',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='quoted',
            name='source',
            field=models.CharField(default=1, max_length=3000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quoted',
            name='source_url',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quoted',
            name='summary',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
