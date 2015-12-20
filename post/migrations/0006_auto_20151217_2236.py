# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
        ('person', '0003_auto_20151217_1916'),
        ('programs', '0001_initial'),
        ('post', '0005_blog'),
    ]

    operations = [
        migrations.CreateModel(
            name='book_home_page',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, to='wagtailcore.Page', primary_key=True, auto_created=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PostAuthorRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('author', models.ForeignKey(related_name='+', to='person.Person')),
                ('post', modelcluster.fields.ParentalKey(related_name='authors', to='post.Post')),
            ],
        ),
        migrations.CreateModel(
            name='PostSubprogramRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('post', modelcluster.fields.ParentalKey(related_name='subprograms', to='post.Post')),
                ('subprogram', models.ForeignKey(related_name='+', to='programs.Subprogram')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='post_author',
            field=models.ManyToManyField(blank=True, through='post.PostAuthorRelationship', to='person.Person'),
        ),
        migrations.AddField(
            model_name='post',
            name='post_subprogram',
            field=models.ManyToManyField(blank=True, through='post.PostSubprogramRelationship', to='programs.Subprogram'),
        ),
    ]
