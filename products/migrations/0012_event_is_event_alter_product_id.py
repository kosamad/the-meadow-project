# Generated by Django 5.0.6 on 2024-07-08 10:33

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_event_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_event',
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]