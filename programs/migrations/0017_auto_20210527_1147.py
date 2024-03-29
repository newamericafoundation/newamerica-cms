# Generated by Django 3.2.3 on 2021-05-27 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0016_auto_20210113_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='fellowship',
            field=models.BooleanField(blank=True, help_text='Select if this is a fellowship program', null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='location',
            field=models.BooleanField(blank=True, help_text='Select if location based program i.e. New America NYC', null=True),
        ),
        migrations.AlterField(
            model_name='subprogram',
            name='fellowship',
            field=models.BooleanField(blank=True, help_text='Select if this is a fellowship program', null=True),
        ),
        migrations.AlterField(
            model_name='subprogram',
            name='location',
            field=models.BooleanField(blank=True, help_text='Select if location based program i.e. New America NYC', null=True),
        ),
    ]
