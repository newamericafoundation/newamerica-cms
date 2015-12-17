# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0001_initial'),
        ('post', '0005_blog'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostSubprogramRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('post', modelcluster.fields.ParentalKey(related_name='subprograms', to='post.Post')),
                ('subprogram', models.ForeignKey(related_name='+', to='programs.Subprogram')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='post_subprogram',
            field=models.ManyToManyField(through='post.PostSubprogramRelationship', blank=True, to='programs.Subprogram'),
        ),
    ]
