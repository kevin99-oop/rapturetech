from django.conf import settings
from django. db. models. signals import post_save 
from django. dispatch import receiver 
from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
import string
import random
from django.utils import timezone
from datetime import timedelta
from datetime import datetime, timedelta
from django.forms.models import model_to_dict
from threading import Timer
import logging
from django.db import models, transaction

import json

# Signal to create a Token for a user upon registration
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token. objects.create(user=instance)

# Model representing a DPU (Data Processing Unit)
# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Model representing a DPU (Data Processing Unit)
class DPU(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dpu_user = models.IntegerField()
    zone = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    st_id = models.CharField(max_length=50, unique=True, primary_key=True)
    society = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15, unique=True)
    owner = models.CharField(max_length=255)
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('deactivated', 'Deactivated'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    date = models.DateTimeField(auto_now_add=True)
    plain_password = models.CharField(max_length=100)

    SELECT_DPU_CHOICES = [
        ('DPMCU', 'DPMCU'),
        ('BMC', 'BMC'),
    ]
    select_dpu = models.CharField(max_length=5, choices=SELECT_DPU_CHOICES, default='DPMCU')

    def __str__(self):
        return f"{self.user.username}'s DPU - {self.st_id}"

    def get_latest_csv_path(self):
        try:
            latest_customer = Customer.objects.filter(st_id=self.st_id).latest('date_uploaded')
            return latest_customer.csv_file.path
        except Customer.DoesNotExist:
            return None
        

class OldDrecDataEdited(models.Model):
    new_drec = models.IntegerField(null=True)
    REC_TYPE = models.CharField(max_length=255)
    SLIP_TYPE = models.IntegerField(null=True, default=None)
    ST_ID = models.CharField(max_length=255)
    CUST_ID = models.IntegerField(null=True, default=None)
    TotalFileRecord = models.IntegerField(null=True, default=None)
    FlagEdited = models.CharField(max_length=10, default="", blank=True)
    MType = models.CharField(max_length=255, null=True, default=None)
    RecordingDate = models.DateField(null=True, default=None)
    RecordingTime = models.CharField(max_length=255, default="0000")
    SHIFT = models.CharField(max_length=255, null=True, default=None)
    FAT = models.FloatField(null=True, default=None)
    FAT_UNIT = models.CharField(max_length=255, default="", blank=True)
    SNF = models.FloatField(null=True, default=None)
    SNF_UNIT = models.CharField(max_length=255, default="", blank=True)
    CLR = models.FloatField(null=True, default=None)
    CLR_UNIT = models.CharField(max_length=255, default="", blank=True)
    WATER = models.FloatField(null=True, default=None)
    WATER_UNIT = models.CharField(max_length=255, default="", blank=True)
    QT = models.FloatField(null=True, default=None)
    QT_UNIT = models.CharField(max_length=255, default="", blank=True)
    RATE = models.FloatField(null=True, default=None)
    Amount = models.FloatField(null=True, default=None)
    CAmount = models.FloatField(null=True, default=None)
    CSR_NO = models.IntegerField(null=True, default=None)
    CREV = models.IntegerField(null=True, default=None)
    END_TAG = models.CharField(max_length=255, default="", blank=True)
    dpuid = models.CharField(max_length=255, default="", blank=True)
    RID = models.CharField(max_length=255, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OldDrecDataEdited for DREC ID: {self.id}"

class DREC(models.Model):
    SLIP_TYPE_CHOICES = [
        (1, 'FAT/SNF/CLR Record'),
        (2, 'Edited FAT/SNF/CLR Data'),
        (3, 'Local Sell'),
        (4, 'Edited Local Sell'),
        (5, 'Dan'),
        (6, 'Edited Dan'),
        (7, 'Deduction'),
    ]

    REC_TYPE = models.CharField(max_length=255, null=True, default=None)
    SLIP_TYPE = models.IntegerField(choices=SLIP_TYPE_CHOICES, default=1)
    ST_ID = models.ForeignKey('DPU', on_delete=models.CASCADE, related_name='drecs')
    CUST_ID = models.IntegerField(null=True, default=None)
    TotalFileRecord = models.IntegerField(null=True, default=None)
    FlagEdited = models.CharField(max_length=10, default="", blank=True)
    MType = models.CharField(max_length=255, null=True, default=None)
    RecordingDate = models.DateField(null=True, default=None)
    RecordingTime = models.CharField(max_length=255, default="0000")
    SHIFT = models.CharField(max_length=255, null=True, default=None)
    FAT = models.FloatField(null=True, default=None)
    FAT_UNIT = models.CharField(max_length=255, default="", blank=True)
    SNF = models.FloatField(null=True, default=None)
    SNF_UNIT = models.CharField(max_length=255, default="", blank=True)
    CLR = models.FloatField(null=True, default=None)
    CLR_UNIT = models.CharField(max_length=255, default="", blank=True)
    WATER = models.FloatField(null=True, default=None)
    WATER_UNIT = models.CharField(max_length=255, default="", blank=True)
    QT = models.FloatField(null=True, default=None)
    QT_UNIT = models.CharField(max_length=255, default="", blank=True)
    RATE = models.FloatField(null=True, default=None)
    Amount = models.FloatField(null=True, default=None)
    CAmount = models.FloatField(null=True, default=None)
    CSR_NO = models.IntegerField(null=True, default=None)
    CREV = models.IntegerField(null=True, default=None)
    END_TAG = models.CharField(max_length=255, default="", blank=True)
    dpuid = models.CharField(max_length=255, default="", blank=True)
    RID = models.CharField(max_length=255, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def get_text_color(self):
        if self.FlagEdited == '1' and self.SLIP_TYPE == 2:
            if self.created_at + timezone.timedelta(minutes=10) > timezone.now():
                return 'green'
            else:
                return ''
        elif self.FlagEdited == 'red':
            return 'red'
        else:
            return ''

    def save(self, *args, **kwargs):
        skip_duplicate_check = kwargs.pop('skip_duplicate_check', False)
        is_update = self.pk is not None

        self.RecordingTime = self.convert_to_hhmm_format(self.RecordingTime)

        if not skip_duplicate_check and not is_update:
            if DREC.objects.filter(
                ST_ID=self.ST_ID,
                REC_TYPE=self.REC_TYPE,
                SLIP_TYPE=self.SLIP_TYPE,
                CUST_ID=self.CUST_ID,
                TotalFileRecord=self.TotalFileRecord,
                MType=self.MType,
                RecordingDate=self.RecordingDate,
                RecordingTime=self.RecordingTime,
                SHIFT=self.SHIFT,
                FAT=self.FAT,
                FAT_UNIT=self.FAT_UNIT,
                SNF=self.SNF,
                SNF_UNIT=self.SNF_UNIT,
                CLR=self.CLR,
                CLR_UNIT=self.CLR_UNIT,
                WATER=self.WATER,
                WATER_UNIT=self.WATER_UNIT,
                QT=self.QT,
                QT_UNIT=self.QT_UNIT,
                RATE=self.RATE,
                Amount=self.Amount,
                CAmount=self.CAmount,
                CSR_NO=self.CSR_NO,
                CREV=self.CREV,
                END_TAG=self.END_TAG,
                dpuid=self.dpuid,
                RID=self.RID
            ).exists():
                raise ValidationError("Duplicate record exists. Record not saved.")

        super().save(*args, **kwargs)


    def convert_to_hhmm_format(self, time_str):
        if len(time_str) == 4:
            return f"{time_str[:2]}:{time_str[2:]}"
        return time_str


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    st_id = models.ForeignKey(DPU, on_delete=models.CASCADE, related_name='customers')
    csv_file = models.FileField(upload_to='csv_files/')
    date_uploaded = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Customer CSV for {self.user.username} - {self.st_id}"

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['st_id']),
            # Add more indexes as needed
        ]

class CustomerList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    st_id = models.CharField(max_length=20)  # Assuming st_id can be up to 20 characters
    cust_id = models.IntegerField()
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    adhaar = models.CharField(max_length=20)
    bank_ac = models.CharField(max_length=30)
    ifsc = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.st_id} - {self.name}"
    def __str__(self):
        return self.name

    @classmethod
    def create_from_csv_line(cls, user, st_id, csv_line):
        data = csv_line.split(',')
        cust_id, name, mobile, adhaar, bank_ac, ifsc = data

        return cls.objects.create(
            user=user,
            st_id=st_id,
            cust_id=cust_id,
            name=name,
            mobile=mobile,
            adhaar=adhaar,
            bank_ac=bank_ac,
            ifsc=ifsc,
        )

# Model representing Configurations
class Config(models.Model):
    user = models.CharField(max_length=255)  # Change this field based on your user model
    st_id = models.CharField(max_length=50, blank=True, null=True)  # Change this field based on your user model
    text_data = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def get_download_url(self):
        # Method to generate download URL for the configuration
        if self.st_id:
            return reverse('download_config', kwargs={'st_id': self.st_id})
        return ''
        
    def __str__(self):
        return f"Config for {self.user} - {self.timestamp}"

class RateTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    animal_type = models.CharField(max_length=100)
    rate_type = models.CharField(max_length=100)
    csv_file = models.FileField(upload_to='rate_tables/')
    start_date = models.DateField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.animal_type} - {self.rate_type}'

    
    @property
    def csv_file_path(self):
        return self.csv_file.path if self.csv_file else ''
    
class Questions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Linking with the User model
    description = models.CharField(max_length=500)
    admin_comment = models.CharField(max_length=200, default='Nothing')
    asked_date = models.DateField(auto_now=True)
    username = models.CharField(max_length=50, null=True, blank=True)  # Add username field
    st_id = models.CharField(max_length=50, null=True, blank=True)  # Add st_id field

    @classmethod
    def delete_old_records(cls):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        cls.objects.filter(asked_date__lt=thirty_days_ago).delete()

@receiver(post_save, sender=Questions)
def set_st_id(sender, instance, created, **kwargs):
    if created:
        try:
            # Get the associated DPU instance based on matching username and mobile_number
            dpu_instance = DPU.objects.get(user__username=instance.username, mobile_number=instance.user_id)
            instance.st_id = dpu_instance.st_id
            instance.save()
        except DPU.DoesNotExist:
            pass
