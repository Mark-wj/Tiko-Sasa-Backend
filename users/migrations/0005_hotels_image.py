# Generated by Django 4.2.18 on 2025-02-07 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_event_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotels',
            name='image',
            field=models.CharField(default='https://tinyurl.com/yck7bwv8', max_length=240),
            preserve_default=False,
        ),
    ]
