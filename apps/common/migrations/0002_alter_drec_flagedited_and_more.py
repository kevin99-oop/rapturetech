# Generated by Django 4.2.9 on 2024-06-01 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drec',
            name='FlagEdited',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='olddrecdataedited',
            name='FlagEdited',
            field=models.BooleanField(default=False),
        ),
    ]
