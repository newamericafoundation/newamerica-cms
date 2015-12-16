# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20151216_1904'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('post_ptr', models.OneToOneField(serialize=False, auto_created=True, parent_link=True, primary_key=True, to='post.Post')),
            ],
            options={
                'abstract': False,
            },
            bases=('post.post',),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('post_ptr', models.OneToOneField(serialize=False, auto_created=True, parent_link=True, primary_key=True, to='post.Post')),
            ],
            options={
                'abstract': False,
            },
            bases=('post.post',),
        ),
        migrations.CreateModel(
            name='Podcasts',
            fields=[
                ('post_ptr', models.OneToOneField(serialize=False, auto_created=True, parent_link=True, primary_key=True, to='post.Post')),
            ],
            options={
                'abstract': False,
            },
            bases=('post.post',),
        ),
        migrations.CreateModel(
            name='PolicyPaper',
            fields=[
                ('post_ptr', models.OneToOneField(serialize=False, auto_created=True, parent_link=True, primary_key=True, to='post.Post')),
            ],
            options={
                'abstract': False,
            },
            bases=('post.post',),
        ),
    ]
