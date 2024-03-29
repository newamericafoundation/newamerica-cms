# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-03 19:36
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.contrib.table_block.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20170118_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgsimplepage',
            name='data_project_external_script',
            field=models.CharField(blank=True, help_text='Specify the name of the external script file within the na-data-projects/projects AWS directory to include that script in the body of the document.', max_length=140, null=True),
        ),
        migrations.AddField(
            model_name='programsimplepage',
            name='data_project_external_script',
            field=models.CharField(blank=True, help_text='Specify the name of the external script file within the na-data-projects/projects AWS directory to include that script in the body of the document.', max_length=140, null=True),
        ),
    ]
