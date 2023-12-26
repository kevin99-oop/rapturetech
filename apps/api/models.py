from django.db import models

class CtRecord(models.Model):
    # Add fields specific to CtRecord model
    field_name = models.CharField(max_length=255)

class DRecord(models.Model):
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
        return f"{self.REC_TYPE} - {self.ST_ID} - {self.RecordingDate}"

class DpuAsKcs(models.Model):
    # Add fields specific to DpuAsKcs model
    field_name = models.CharField(max_length=255)

class Dpus(models.Model):
    # Add fields specific to Dpus model
    field_name = models.CharField(max_length=255)

class RateTableAlls(models.Model):
    # Add fields specific to RateTableAlls model
    field_name = models.CharField(max_length=255)

class RateTables(models.Model):
    # Add fields specific to RateTables model
    field_name = models.CharField(max_length=255)