# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
        ('programs', '0002_auto_20151221_2222'),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpertPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='OurPeoplePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Homepage for all People in NAF',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ProgramPeoplePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Our People Page for Programs',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='person',
            name='expert',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='program',
            field=models.ForeignKey(blank=True, to='programs.Program', null=True),
        ),
    ]
