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
    dpu = models.ForeignKey(DPU, on_delete=models.CASCADE)
    st_id = models.CharField(max_length=50)
    # ... (other fields from your JSON data)
    recording_date = models.DateField()
    shift = models.CharField(max_length=50)
    fat = models.FloatField()
    fat_unit = models.CharField(max_length=50)
    snf = models.FloatField()
    snf_unit = models.CharField(max_length=50)
    clr = models.FloatField()
    clr_unit = models.CharField(max_length=50)
    water = models.FloatField()
    water_unit = models.CharField(max_length=50)
    qt = models.FloatField()
    qt_unit = models.CharField(max_length=50)
    rate = models.FloatField()
    amount = models.FloatField()
    camount = models.FloatField()
    csr_no = models.IntegerField()
    crev = models.IntegerField()
    end_tag = models.CharField(max_length=50)
    dpuid = models.CharField(max_length=50)
    data = models.JSONField()

    def __str__(self):
        return f"DREC for {self.dpu.user.username} - {self.st_id}"
    
    def formatted_recording_date(self):
        return self.recording_date.strftime("%Y-%m-%d")