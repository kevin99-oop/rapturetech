# Generated by Django 4.2.9 on 2024-06-15 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0020_rename_old_drec_olddrecdataedited_new_drec'),
    ]

    operations = [
        migrations.AddField(
            model_name='dpu',
            name='check_options',
            field=models.TextField(default=''),
        ),
    ]
