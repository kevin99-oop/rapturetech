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

class Drec(models.Model):
    REC_TYPE = models.CharField(max_length=1)
    SLIP_TYPE = models.CharField(max_length=1)
    ST_ID = models.CharField(max_length=255)
    CUST_ID = models.IntegerField()
    TotalFileRecord = models.IntegerField()
    FlagEdited = models.CharField(max_length=1)
    MType = models.CharField(max_length=1)
    RecordingDate = models.DateField()
    SHIFT = models.CharField(max_length=1)
    FAT = models.FloatField()
    FAT_UNIT = models.CharField(max_length=1)
    SNF = models.FloatField()
    SNF_UNIT = models.CharField(max_length=1)
    CLR = models.FloatField()
    CLR_UNIT = models.CharField(max_length=1)
    WATER = models.FloatField()
    WATER_UNIT = models.CharField(max_length=1)
    QT = models.FloatField()
    QT_UNIT = models.CharField(max_length=1)
    RATE = models.FloatField()
    Amount = models.FloatField()
    CAmount = models.FloatField()
    CSR_NO = models.IntegerField()
    CREV = models.IntegerField()
    END_TAG = models.CharField(max_length=1)
    dpuid = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.REC_TYPE} - {self.ST_ID} - {self.CUST_ID}"