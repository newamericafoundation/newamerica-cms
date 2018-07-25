# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-18 15:46
from __future__ import unicode_literals

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0011_auto_20180718_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='feature_carousel',
            field=wagtail.core.fields.StreamField((('page', wagtail.core.blocks.PageChooserBlock()),), blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='sidebar_menu_about_us_pages',
            field=wagtail.core.fields.StreamField((('Item', wagtail.core.blocks.PageChooserBlock()),), blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='sidebar_menu_initiatives_and_projects_pages',
            field=wagtail.core.fields.StreamField((('Item', wagtail.core.blocks.PageChooserBlock()),), blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='sidebar_menu_our_work_pages',
            field=wagtail.core.fields.StreamField((('Item', wagtail.core.blocks.PageChooserBlock()),), blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subprogram',
            name='feature_carousel',
            field=wagtail.core.fields.StreamField((('page', wagtail.core.blocks.PageChooserBlock()),), blank=True, null=True),
        ),
    ]
