# Generated by Django 3.0.7 on 2020-12-04 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_auto_20201203_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='intro',
            field=models.CharField(max_length=250),
        ),
    ]
