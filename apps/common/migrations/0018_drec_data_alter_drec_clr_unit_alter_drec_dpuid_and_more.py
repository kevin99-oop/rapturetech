# Generated by Django 4.2.8 on 2023-12-28 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0017_drec'),
    ]

    operations = [
        migrations.AddField(
            model_name='drec',
            name='data',
            field=models.JSONField(default=11),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='drec',
            name='clr_unit',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='drec',
            name='dpuid',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='drec',
            name='end_tag',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='drec',
            name='fat_unit',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='drec',
            name='qt_unit',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='drec',
            name='shift',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='drec',
            name='snf_unit',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='drec',
            name='water_unit',
            field=models.CharField(max_length=50),
        ),
    ]
