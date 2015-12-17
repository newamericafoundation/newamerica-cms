# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_about'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('post_ptr', models.OneToOneField(primary_key=True, to='post.Post', serialize=False, parent_link=True, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('post.post',),
        ),
    ]
