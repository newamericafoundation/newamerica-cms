# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_person_program'),
        ('programs', '0001_initial'),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postsubprogramrelationship',
            name='subprogram',
            field=models.ForeignKey(to='programs.Subprogram', related_name='+'),
        ),
        migrations.AddField(
            model_name='postprogramrelationship',
            name='post',
            field=modelcluster.fields.ParentalKey(to='post.Post', related_name='programs'),
        ),
        migrations.AddField(
            model_name='postprogramrelationship',
            name='program',
            field=models.ForeignKey(to='programs.Program', related_name='+'),
        ),
        migrations.AddField(
            model_name='postauthorrelationship',
            name='author',
            field=models.ForeignKey(to='person.Person', related_name='+'),
        ),
        migrations.AddField(
            model_name='postauthorrelationship',
            name='post',
            field=modelcluster.fields.ParentalKey(to='post.Post', related_name='authors'),
        ),
        migrations.AddField(
            model_name='post',
            name='parent_programs',
            field=models.ManyToManyField(blank=True, to='programs.Program', through='post.PostProgramRelationship'),
        ),
        migrations.AddField(
            model_name='post',
            name='post_author',
            field=models.ManyToManyField(blank=True, to='person.Person', through='post.PostAuthorRelationship'),
        ),
        migrations.AddField(
            model_name='post',
            name='post_subprogram',
            field=models.ManyToManyField(blank=True, to='programs.Subprogram', through='post.PostSubprogramRelationship'),
        ),
    ]
