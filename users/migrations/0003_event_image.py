# Generated by Django 4.2.18 on 2025-02-07 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_event_hotels_movies'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.URLField(default='https://tinyurl.com/2s4yswt8'),
            preserve_default=False,
        ),
    ]
