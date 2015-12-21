# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields
import wagtail.wagtailimages.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
        ('programs', '0002_auto_20151221_2222'),
        ('person', '0002_auto_20151221_2222'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('date', models.DateField(verbose_name=b'Post date')),
                ('body', wagtail.wagtailcore.fields.StreamField([(b'heading', wagtail.wagtailcore.blocks.CharBlock(classname=b'full title')), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), (b'html', wagtail.wagtailcore.blocks.RawHTMLBlock()), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock())])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PostAuthorRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.ForeignKey(related_name='+', to='person.Person')),
                ('post', modelcluster.fields.ParentalKey(related_name='authors', to='post.Post')),
            ],
        ),
        migrations.CreateModel(
            name='PostProgramRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post', modelcluster.fields.ParentalKey(related_name='programs', to='post.Post')),
                ('program', models.ForeignKey(related_name='+', to='programs.Program')),
            ],
        ),
        migrations.CreateModel(
            name='PostSubprogramRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post', modelcluster.fields.ParentalKey(related_name='subprograms', to='post.Post')),
                ('subprogram', models.ForeignKey(related_name='+', to='programs.Subprogram')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='parent_programs',
            field=models.ManyToManyField(to='programs.Program', through='post.PostProgramRelationship', blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_author',
            field=models.ManyToManyField(to='person.Person', through='post.PostAuthorRelationship', blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_subprogram',
            field=models.ManyToManyField(to='programs.Subprogram', through='post.PostSubprogramRelationship', blank=True),
        ),
    ]
