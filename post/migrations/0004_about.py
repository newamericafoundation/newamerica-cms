# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_article_event_podcasts_policypaper'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('post_ptr', models.OneToOneField(parent_link=True, serialize=False, auto_created=True, primary_key=True, to='post.Post')),
            ],
            options={
                'abstract': False,
            },
            bases=('post.post',),
        ),
    ]
