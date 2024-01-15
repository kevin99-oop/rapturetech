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
    dpu_id = models.CharField(max_length=50, unique=True)
    society = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    owner = models.CharField(max_length=255)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('deactivated', 'Deactivated'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.user.username}'s DPU - {self.dpu_id}"
class DREC(models.Model):
    REC_TYPE = models.CharField(max_length=255, default="", blank=True)
    SLIP_TYPE = models.IntegerField(null=True, default=None)
    ST_ID = models.CharField(max_length=255, default="", blank=True)
    CUST_ID = models.IntegerField(null=True, default=None)
    TotalFileRecord = models.IntegerField(null=True, default=None)
    FlagEdited = models.CharField(max_length=255, default="", blank=True)
    MType = models.IntegerField(null=True, default=None)
    RecordingDate = models.DateField(null=True, default=None)
    SHIFT = models.IntegerField(null=True, default=None)
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
    dpuid = models.ForeignKey(DPU, on_delete=models.CASCADE, to_field='dpu_id')

    def __str__(self):
        return f"DREC for {self.dpu.user.username}'s DPU - {self.dpuid.dpu_id}"
