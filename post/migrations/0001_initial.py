# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='book_home_page',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, parent_link=True, to='wagtailcore.Page', primary_key=True, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, parent_link=True, to='wagtailcore.Page', primary_key=True, auto_created=True)),
                ('date', models.DateField(verbose_name='Post date')),
                ('body', wagtail.wagtailcore.fields.StreamField((('heading', wagtail.wagtailcore.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())))),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PostAuthorRelationship',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostProgramRelationship',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostSubprogramRelationship',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('post_ptr', models.OneToOneField(serialize=False, parent_link=True, to='post.Post', primary_key=True, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('post.post',),
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('post_ptr', models.OneToOneField(serialize=False, parent_link=True, to='post.Post', primary_key=True, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('post.post',),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('post_ptr', models.OneToOneField(serialize=False, parent_link=True, to='post.Post', primary_key=True, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('post.post',),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('post_ptr', models.OneToOneField(serialize=False, parent_link=True, to='post.Post', primary_key=True, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('post.post',),
        ),
        migrations.CreateModel(
            name='Podcasts',
            fields=[
                ('post_ptr', models.OneToOneField(serialize=False, parent_link=True, to='post.Post', primary_key=True, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('post.post',),
        ),
        migrations.CreateModel(
            name='PolicyPaper',
            fields=[
                ('post_ptr', models.OneToOneField(serialize=False, parent_link=True, to='post.Post', primary_key=True, auto_created=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('post.post',),
        ),
        migrations.AddField(
            model_name='postsubprogramrelationship',
            name='post',
            field=modelcluster.fields.ParentalKey(to='post.Post', related_name='subprograms'),
        ),
    ]
