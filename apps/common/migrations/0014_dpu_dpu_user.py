# Generated by Django 4.2.9 on 2024-03-21 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0013_remove_dpu_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='dpu',
            name='dpu_user',
            field=models.IntegerField(default=1),
        ),
    ]
