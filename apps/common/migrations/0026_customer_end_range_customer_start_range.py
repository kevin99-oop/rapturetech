# Generated by Django 4.2.9 on 2024-01-20 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0025_customer_related_to_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='end_range',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='customer',
            name='start_range',
            field=models.IntegerField(default=1),
        ),
    ]
