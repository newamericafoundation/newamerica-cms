# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailimages.blocks
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, serialize=False, to='wagtailcore.Page', auto_created=True, parent_link=True)),
                ('name', models.CharField(max_length=100)),
                ('description', wagtail.wagtailcore.fields.StreamField((('heading', wagtail.wagtailcore.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())))),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ProgramSubprogramRelationship',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('program', modelcluster.fields.ParentalKey(related_name='subprograms', to='programs.Program')),
            ],
        ),
        migrations.CreateModel(
            name='Subprogram',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, serialize=False, to='wagtailcore.Page', auto_created=True, parent_link=True)),
                ('name', models.CharField(max_length=100)),
                ('description', wagtail.wagtailcore.fields.StreamField((('heading', wagtail.wagtailcore.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())))),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='programsubprogramrelationship',
            name='subprogram',
            field=models.ForeignKey(to='programs.Subprogram'),
        ),
        migrations.AddField(
            model_name='program',
            name='program_subprograms',
            field=models.ManyToManyField(blank=True, to='programs.Subprogram', through='programs.ProgramSubprogramRelationship'),
        ),
    ]
