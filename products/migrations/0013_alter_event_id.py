# Generated by Django 5.0.6 on 2024-07-08 10:37

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_event_is_event_alter_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
