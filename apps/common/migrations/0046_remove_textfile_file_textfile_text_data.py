# Generated by Django 4.2.9 on 2024-01-25 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0045_customer_date_uploaded'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textfile',
            name='file',
        ),
        migrations.AddField(
            model_name='textfile',
            name='text_data',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
