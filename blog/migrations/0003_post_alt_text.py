# Generated by Django 5.0.6 on 2024-07-24 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='alt_text',
            field=models.TextField(default=''),
        ),
    ]
