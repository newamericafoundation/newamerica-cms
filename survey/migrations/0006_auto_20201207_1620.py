# Generated by Django 3.0.7 on 2020-12-07 21:20

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_surveyhomepage_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='intro',
        ),
        migrations.AddField(
            model_name='survey',
            name='demos_key',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='findings',
            field=wagtail.core.fields.RichTextField(blank=True, max_length=12500, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='org',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='sample_demos',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='sample_number',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='sample_size',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='study_title',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
