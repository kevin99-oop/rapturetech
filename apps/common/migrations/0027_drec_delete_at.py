# Generated by Django 4.2.9 on 2024-06-21 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0026_localsell_clr_localsell_clr_unit_localsell_fat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='drec',
            name='delete_at',
            field=models.DateTimeField(null=True),
        ),
    ]
