# Generated by Django 3.2.18 on 2025-04-16 18:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('future_security_forum', '0006_auto_20250416_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='savethedatepage',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Start Date'),
        ),
        migrations.AddField(
            model_name='savethedatepage',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
