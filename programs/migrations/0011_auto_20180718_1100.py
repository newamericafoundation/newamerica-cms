# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-18 15:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0010_auto_20180424_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='feature_carousel',
            field=wagtail.core.fields.StreamField((('page', wagtail.core.blocks.PageChooserBlock()),), blank=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='fellowship',
            field=models.NullBooleanField(help_text='Select if this is a fellowship program'),
        ),
        migrations.AlterField(
            model_name='program',
            name='location',
            field=models.NullBooleanField(help_text='Select if location based program i.e. New America NYC'),
        ),
        migrations.AlterField(
            model_name='program',
            name='name',
            field=models.CharField(help_text='Name of Program', max_length=100),
        ),
        migrations.AlterField(
            model_name='program',
            name='sidebar_menu_about_us_pages',
            field=wagtail.core.fields.StreamField((('Item', wagtail.core.blocks.PageChooserBlock()),), blank=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='sidebar_menu_initiatives_and_projects_pages',
            field=wagtail.core.fields.StreamField((('Item', wagtail.core.blocks.PageChooserBlock()),), blank=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='sidebar_menu_our_work_pages',
            field=wagtail.core.fields.StreamField((('Item', wagtail.core.blocks.PageChooserBlock()),), blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='redirect_page',
            field=models.ForeignKey(blank=True, help_text='Select a report or other post that you would like to show up as a project in your Initiatives & Projects list', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page'),
        ),
        migrations.AlterField(
            model_name='subprogram',
            name='feature_carousel',
            field=wagtail.core.fields.StreamField((('page', wagtail.core.blocks.PageChooserBlock()),), blank=True),
        ),
        migrations.AlterField(
            model_name='subprogram',
            name='fellowship',
            field=models.NullBooleanField(help_text='Select if this is a fellowship program'),
        ),
        migrations.AlterField(
            model_name='subprogram',
            name='location',
            field=models.NullBooleanField(help_text='Select if location based program i.e. New America NYC'),
        ),
        migrations.AlterField(
            model_name='subprogram',
            name='name',
            field=models.CharField(help_text='Name of Program', max_length=100),
        ),
        migrations.AlterField(
            model_name='subprogram',
            name='template',
            field=models.CharField(choices=[('programs/program.html', 'Full'), ('simple_program.html', 'Efficiency'), ('programs/program.html', 'Collection')], default='programs/program.html', max_length=100),
        ),
    ]
