# Generated by Django 3.2.18 on 2025-05-12 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_book_publication_cover_image_alt'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='media_link',
            field=models.URLField(blank=True, default=''),
        ),
    ]
