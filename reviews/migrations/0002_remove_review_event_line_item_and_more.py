# Generated by Django 5.0.6 on 2024-08-07 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='event_line_item',
        ),
        migrations.RemoveField(
            model_name='review',
            name='product_line_item',
        ),
    ]
