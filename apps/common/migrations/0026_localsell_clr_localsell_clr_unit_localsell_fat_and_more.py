# Generated by Django 4.2.9 on 2024-06-21 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0025_localsell'),
    ]

    operations = [
        migrations.AddField(
            model_name='localsell',
            name='CLR',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='localsell',
            name='CLR_UNIT',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='localsell',
            name='FAT',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='localsell',
            name='FAT_UNIT',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='localsell',
            name='SNF',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='localsell',
            name='SNF_UNIT',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='localsell',
            name='WATER',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='localsell',
            name='WATER_UNIT',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
