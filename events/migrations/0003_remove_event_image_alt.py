# Generated by Django 3.2.25 on 2024-06-25 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20240625_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='image_alt',
        ),
    ]
