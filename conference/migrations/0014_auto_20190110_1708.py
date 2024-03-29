# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-10 22:08
from __future__ import unicode_literals

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0013_auto_20180718_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='sessions',
            field=wagtail.fields.StreamField([('days', wagtail.blocks.StructBlock([('collapsible', wagtail.blocks.BooleanBlock(default=True, help_text='Allow schedule sessions to expand and collapse', required=False)), ('day', wagtail.blocks.ChoiceBlock(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], help_text='What day of the conference is this session on?', required=False)), ('start_time', wagtail.blocks.TimeBlock(required=False)), ('end_time', wagtail.blocks.TimeBlock(required=False)), ('sessions', wagtail.blocks.StreamBlock([('session', wagtail.blocks.StructBlock([('name', wagtail.blocks.TextBlock(required=False)), ('description', wagtail.blocks.RichTextBlock(required=False)), ('start_time', wagtail.blocks.TimeBlock(required=False)), ('end_time', wagtail.blocks.TimeBlock(required=False)), ('speakers', wagtail.blocks.StreamBlock([('speaker', wagtail.blocks.StructBlock([('name', wagtail.blocks.TextBlock(required=False)), ('twitter', wagtail.blocks.URLBlock(required=False)), ('title', wagtail.blocks.TextBlock(required=False))]))], required=False)), ('archived_video_link', wagtail.blocks.URLBlock(help_text='Enter youtube link after conference', required=False))]))]))], help_text='for multi-day events'))], blank=True, null=True),
        ),
    ]
