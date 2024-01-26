# Generated by Django 4.2.9 on 2024-01-26 12:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_remove_config_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='config',
            name='st_id',
        ),
        migrations.AddField(
            model_name='config',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
