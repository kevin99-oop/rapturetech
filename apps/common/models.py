from django.conf import settings
from django. db. models. signals import post_save 
from django. dispatch import receiver 
from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import User

@receiver (post_save, sender=settings. AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token. objects.create(user=instance)


class DPU(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    st_id = models.CharField(max_length=50, unique=True, primary_key=True)  # Renamed from dpu_id to st_id
    society = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    owner = models.CharField(max_length=255)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('deactivated', 'Deactivated'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    date = models.DateTimeField(auto_now_add=True)  # Automatically set on creation

    def __str__(self):
        return f"{self.user.username}'s DPU - {self.st_id}"


class DREC(models.Model):
    REC_TYPE = models.CharField(max_length=255, default="", blank=True)
    SLIP_TYPE = models.IntegerField(null=True, default=None)
    ST_ID = models.OneToOneField(DPU, on_delete=models.CASCADE, primary_key=True)  # Updated to OneToOneField
    CUST_ID = models.IntegerField(null=True, default=None)
    TotalFileRecord = models.IntegerField(null=True, default=None)
    FlagEdited = models.CharField(max_length=255, default="", blank=True)
    MType = models.CharField(max_length=255,null=True, default=None)
    RecordingDate = models.DateField(null=True, default=None)
    SHIFT = models.CharField(max_length=255,null=True, default=None)
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

    def __str__(self):
        return f"DREC for {self.ST_ID.user.username}'s DPU - {self.ST_ID.st_id}"
    
