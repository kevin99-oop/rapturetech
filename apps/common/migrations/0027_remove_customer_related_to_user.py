# Generated by Django 4.2.9 on 2024-01-20 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0026_customer_end_range_customer_start_range'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='related_to_user',
        ),
    ]
