# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
        ('person', '0002_person_program'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpertPage',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, to='wagtailcore.Page', primary_key=True, auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='OurPeoplePage',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, to='wagtailcore.Page', primary_key=True, auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ProgramPeoplePage',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, to='wagtailcore.Page', primary_key=True, auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='person',
            name='expert',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
