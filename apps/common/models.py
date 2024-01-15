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
    REC_TYPE = models.CharField(max_length=100, null=True, blank=True)
    SLIP_TYPE = models.CharField(max_length=100, null=True, blank=True)
    ST_ID = models.CharField(max_length=5000, null=True, blank=True)
    CUST_ID = models.IntegerField(null=True, blank=True)
    TotalFileRecord = models.IntegerField(null=True, blank=True)
    FlagEdited = models.CharField(max_length=100, null=True, blank=True)
    MType = models.CharField(max_length=100, null=True, blank=True)
    RecordingDate = models.DateField(null=True, blank=True)
    SHIFT = models.CharField(max_length=100, null=True, blank=True)
    FAT = models.FloatField(null=True, blank=True)
    FAT_UNIT = models.CharField(max_length=100, null=True, blank=True)
    SNF = models.FloatField(null=True, blank=True)
    SNF_UNIT = models.CharField(max_length=100, null=True, blank=True)
    CLR = models.FloatField(null=True, blank=True)
    CLR_UNIT = models.CharField(max_length=100, null=True, blank=True)
    WATER = models.FloatField(null=True, blank=True)
    WATER_UNIT = models.CharField(max_length=100, null=True, blank=True)
    QT = models.FloatField(null=True, blank=True)
    QT_UNIT = models.CharField(max_length=100, null=True, blank=True)
    RATE = models.FloatField(null=True, blank=True)
    Amount = models.FloatField(null=True, blank=True)
    CAmount = models.FloatField(null=True, blank=True)
    CSR_NO = models.IntegerField(null=True, blank=True)
    CREV = models.IntegerField(null=True, blank=True)
    END_TAG = models.CharField(max_length=100, null=True, blank=True)
    dpuid = models.OneToOneField(DPU, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"DREC for {self.dpuid.user.username}'s DPU - {self.dpuid.dpu_id}"