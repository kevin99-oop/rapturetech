from django.conf import settings
from django. db. models. signals import post_save 
from django. dispatch import receiver 
from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError

# Signal to create a Token for a user upon registration
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token. objects.create(user=instance)

# Model representing a DPU (Data Processing Unit)
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
    def get_latest_csv_path(self):
            try:
                latest_customer = Customer.objects.filter(st_id=self.st_id).latest('date_uploaded')
                return latest_customer.csv_file.path
            except Customer.DoesNotExist:
                return None

# Model representing DREC (Data Recording)
class DREC(models.Model):
    REC_TYPE = models.CharField(max_length=255, default="", blank=True)
    SLIP_TYPE = models.IntegerField(null=True, default=None)
    ST_ID = models.ForeignKey(DPU, on_delete=models.CASCADE, related_name='drecs')  # Use ForeignKey instead of OneToOneField
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
    
        
    def save(self, *args, **kwargs):
            # Check the status of the associated DPU
            if self.ST_ID.status == 'deactivated':
                raise ValidationError("Cannot save DREC. DPU is deactivated. Activate the DPU from the admin.")
            
            super().save(*args, **kwargs)
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
    

