# Generated by Django 4.2.18 on 2025-02-07 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.CharField(max_length=240),
        ),
    ]
