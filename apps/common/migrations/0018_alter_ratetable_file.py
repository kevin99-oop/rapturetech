# Generated by Django 4.2.9 on 2024-02-15 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0017_alter_ratetable_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratetable',
            name='file',
            field=models.FileField(upload_to='rate_tables/'),
        ),
    ]
