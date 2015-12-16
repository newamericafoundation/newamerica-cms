# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
        ('programs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postprogramrelationship',
            name='program',
            field=models.ForeignKey(to='programs.Program', related_name='+'),
        ),
        migrations.AddField(
            model_name='post',
            name='parent_programs',
            field=models.ManyToManyField(to='programs.Program', blank=True, through='post.PostProgramRelationship'),
        ),
    ]
