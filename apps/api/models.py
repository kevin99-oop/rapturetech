from django.db import models

class CtRecord(models.Model):
    # Add fields specific to CtRecord model
    field_name = models.CharField(max_length=255)

class DRecord(models.Model):
    # Add fields specific to DRecord model
    field_name = models.CharField(max_length=255)

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