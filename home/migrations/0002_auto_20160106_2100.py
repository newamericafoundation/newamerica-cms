# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
        ('programs', '0001_initial'),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postsubprogramrelationship',
            name='subprogram',
            field=models.ForeignKey(related_name='+', to='programs.Subprogram'),
        ),
        migrations.AddField(
            model_name='postprogramrelationship',
            name='post',
            field=modelcluster.fields.ParentalKey(related_name='programs', to='home.Post'),
        ),
        migrations.AddField(
            model_name='postprogramrelationship',
            name='program',
            field=models.ForeignKey(related_name='+', to='programs.Program'),
        ),
        migrations.AddField(
            model_name='postauthorrelationship',
            name='author',
            field=models.ForeignKey(related_name='+', to='person.Person'),
        ),
        migrations.AddField(
            model_name='postauthorrelationship',
            name='post',
            field=modelcluster.fields.ParentalKey(related_name='authors', to='home.Post'),
        ),
        migrations.AddField(
            model_name='post',
            name='parent_programs',
            field=models.ManyToManyField(to='programs.Program', through='home.PostProgramRelationship', blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_author',
            field=models.ManyToManyField(to='person.Person', through='home.PostAuthorRelationship', blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_subprogram',
            field=models.ManyToManyField(to='programs.Subprogram', through='home.PostSubprogramRelationship', blank=True),
        ),
    ]
