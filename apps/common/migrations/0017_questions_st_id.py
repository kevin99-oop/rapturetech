# Generated by Django 4.2.9 on 2024-05-09 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0016_alter_questions_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='st_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
