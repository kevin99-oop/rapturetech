# Generated by Django 4.2.8 on 2023-12-11 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('common', '0013_user_groups_user_is_active_user_is_staff_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='CustomUser',
        ),
    ]
