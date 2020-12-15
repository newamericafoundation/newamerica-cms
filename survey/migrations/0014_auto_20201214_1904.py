# Generated by Django 3.0.7 on 2020-12-15 00:04

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailcore', '0052_pagelogentry'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('survey', '0013_auto_20201214_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey_orgs',
            name='title',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='survey',
            name='org',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='Survey_Orgs', to='survey.Survey_Orgs'),
        ),
        migrations.DeleteModel(
            name='Survey_Orgs_Index',
        ),
    ]
