# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0002_auto_20151216_0400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='program',
            name='program_subprograms',
        ),
        migrations.AddField(
            model_name='subprogram',
            name='parent_programs',
            field=models.ManyToManyField(blank=True, to='programs.Program', through='programs.ProgramSubprogramRelationship'),
        ),
        migrations.AlterField(
            model_name='programsubprogramrelationship',
            name='program',
            field=models.ForeignKey(related_name='+', to='programs.Program'),
        ),
        migrations.AlterField(
            model_name='programsubprogramrelationship',
            name='subprogram',
            field=modelcluster.fields.ParentalKey(related_name='programs', to='programs.Subprogram'),
        ),
    ]
