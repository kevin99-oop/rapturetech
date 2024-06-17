# Generated by Django 4.2.9 on 2024-06-16 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0023_alter_dpu_check_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='OldDrecDataDeleted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_drec', models.IntegerField(null=True)),
                ('REC_TYPE', models.CharField(max_length=255)),
                ('SLIP_TYPE', models.IntegerField(default=None, null=True)),
                ('ST_ID', models.CharField(max_length=255)),
                ('CUST_ID', models.IntegerField(default=None, null=True)),
                ('TotalFileRecord', models.IntegerField(default=None, null=True)),
                ('FlagEdited', models.CharField(blank=True, default='', max_length=10)),
                ('MType', models.CharField(default=None, max_length=255, null=True)),
                ('RecordingDate', models.DateField(default=None, null=True)),
                ('RecordingTime', models.CharField(default='0000', max_length=255)),
                ('SHIFT', models.CharField(default=None, max_length=255, null=True)),
                ('FAT', models.FloatField(default=None, null=True)),
                ('FAT_UNIT', models.CharField(blank=True, default='', max_length=255)),
                ('SNF', models.FloatField(default=None, null=True)),
                ('SNF_UNIT', models.CharField(blank=True, default='', max_length=255)),
                ('CLR', models.FloatField(default=None, null=True)),
                ('CLR_UNIT', models.CharField(blank=True, default='', max_length=255)),
                ('WATER', models.FloatField(default=None, null=True)),
                ('WATER_UNIT', models.CharField(blank=True, default='', max_length=255)),
                ('QT', models.FloatField(default=None, null=True)),
                ('QT_UNIT', models.CharField(blank=True, default='', max_length=255)),
                ('RATE', models.FloatField(default=None, null=True)),
                ('Amount', models.FloatField(default=None, null=True)),
                ('CAmount', models.FloatField(default=None, null=True)),
                ('CSR_NO', models.IntegerField(default=None, null=True)),
                ('CREV', models.IntegerField(default=None, null=True)),
                ('END_TAG', models.CharField(blank=True, default='', max_length=255)),
                ('dpuid', models.CharField(blank=True, default='', max_length=255)),
                ('RID', models.CharField(default=None, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
