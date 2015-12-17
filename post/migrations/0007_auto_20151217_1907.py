# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_person_program'),
        ('post', '0006_auto_20151217_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostAuthorRelationship',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('author', models.ForeignKey(to='person.Person', related_name='+')),
                ('post', modelcluster.fields.ParentalKey(to='post.Post', related_name='authors')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='post_author',
            field=models.ManyToManyField(to='person.Person', blank=True, through='post.PostAuthorRelationship'),
        ),
    ]
