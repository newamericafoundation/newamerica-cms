# Generated by Django 3.2.18 on 2024-06-28 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0065_accordion_blocks'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='apply_smart_punctuation',
            field=models.BooleanField(default=False, help_text='Change straight quote characters into curly quote characters'),
        ),
    ]