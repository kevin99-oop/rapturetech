from django.contrib import admin

# Register your models here.
from apps.common.models import DREC,DPU,Customer,Config
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import csv
class DPUAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'dpu_id', 'society', 'mobile_number', 'owner', 'status', 'Amount', 'CAmount')
@admin.register(DREC)
class DRECAdmin(admin.ModelAdmin):
    list_display = ('REC_TYPE', 'SLIP_TYPE', 'ST_ID', 'CUST_ID', 'RecordingDate', 'SHIFT', 'QT', 'Amount', 'CAmount','dpuid')
    search_fields = ['ST_ID', 'CUST_ID']  # Add fields you want to search on

    # Additional configurations as needed
admin.site.register(DPU)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'st_id', 'csv_file',)
    search_fields = ('user__username', 'st_id')


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('user','st_id','timestamp','text_data')
    search_fields = ('user',)  # Enable searching by username
    
