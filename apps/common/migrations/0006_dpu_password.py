# Generated by Django 4.2.9 on 2024-03-15 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_remove_dpu_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='dpu',
            name='password',
            field=models.CharField(default=123, max_length=100),
            preserve_default=False,
        ),
    ]
