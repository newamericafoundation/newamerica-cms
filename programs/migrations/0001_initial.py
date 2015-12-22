# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import modelcluster.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('name', models.CharField(max_length=100)),
                ('description', wagtail.wagtailcore.fields.StreamField([(b'heading', wagtail.wagtailcore.blocks.CharBlock(classname=b'full title')), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), (b'html', wagtail.wagtailcore.blocks.RawHTMLBlock()), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock())])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ProgramSubprogramRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('program', models.ForeignKey(related_name='+', to='programs.Program')),
            ],
        ),
        migrations.CreateModel(
            name='Subprogram',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('name', models.CharField(max_length=100)),
                ('description', wagtail.wagtailcore.fields.StreamField([(b'heading', wagtail.wagtailcore.blocks.CharBlock(classname=b'full title')), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), (b'html', wagtail.wagtailcore.blocks.RawHTMLBlock()), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock())])),
                ('parent_programs', models.ManyToManyField(to='programs.Program', through='programs.ProgramSubprogramRelationship', blank=True)),
            ],
            options={
                'verbose_name': 'Subprogram/Initiative Page',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='programsubprogramrelationship',
            name='subprogram',
            field=modelcluster.fields.ParentalKey(related_name='programs', to='programs.Subprogram'),
        ),
    ]
