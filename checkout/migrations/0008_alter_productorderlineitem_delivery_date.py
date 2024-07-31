# Generated by Django 5.0.6 on 2024-07-31 14:50

import checkout.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0007_order_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorderlineitem',
            name='delivery_date',
            field=models.DateField(blank=True, null=True, validators=[checkout.validators.validate_date]),
        ),
    ]
