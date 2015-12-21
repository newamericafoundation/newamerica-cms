# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20151221_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='PressRelease',
            fields=[
                ('post_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='post.Post')),
            ],
            options={
                'abstract': False,
            },
            bases=('post.post',),
        ),
        migrations.CreateModel(
            name='Quoted',
            fields=[
                ('post_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='post.Post')),
            ],
            options={
                'abstract': False,
            },
            bases=('post.post',),
        ),
        migrations.AlterModelOptions(
            name='bookhomepage',
            options={'verbose_name': 'Homepage for all books'},
        ),
    ]
