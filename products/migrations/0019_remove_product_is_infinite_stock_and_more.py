# Generated by Django 5.0.6 on 2024-08-08 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_remove_productvariant_card_message_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_infinite_stock',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='productvariant',
            name='is_infinite_stock',
        ),
        migrations.RemoveField(
            model_name='productvariant',
            name='stock',
        ),
    ]
