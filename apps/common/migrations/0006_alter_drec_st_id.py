# Generated by Django 4.2.8 on 2024-01-16 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_alter_drec_st_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drec',
            name='ST_ID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='common.dpu'),
        ),
    ]
