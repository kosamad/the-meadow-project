# Generated by Django 5.0.6 on 2024-07-03 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='duration_hours',
            field=models.IntegerField(default=1, verbose_name='Duration (hours)'),
        ),
    ]
