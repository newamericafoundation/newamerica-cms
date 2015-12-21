# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('post_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='post.Post')),
            ],
            options={
                'abstract': False,
            },
            bases=('post.post',),
        ),
    ]
