# Generated by Django 4.2.9 on 2024-03-17 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0011_alter_dpu_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dpu',
            name='mobile_number',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
