# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-12 03:14
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0014_auto_20180807_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='endnotes',
            field=wagtail.fields.StreamField([('endnote', wagtail.blocks.StructBlock([('number', wagtail.blocks.TextBlock()), ('note', wagtail.blocks.RichTextBlock())], null=True, required=False))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='generate_pdf_on_publish',
            field=models.BooleanField(default=False, help_text='⚠ Save latest content before checking this ⚠\nIf checked, the "Report PDF" field will be filled with a generated pdf. Otherwise, leave this unchecked and upload a pdf to the "Report PDF" field.', verbose_name='Generate PDF on save'),
        ),
        migrations.AlterField(
            model_name='report',
            name='overwrite_sections_on_save',
            field=models.BooleanField(default=False, help_text='If checked, sections and endnote fields ⚠ will be overwritten ⚠ with Word document source on save. Use with CAUTION!'),
        ),
    ]
