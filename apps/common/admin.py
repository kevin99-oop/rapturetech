from django.contrib import admin

# Register your models here.
from apps.common.models import DREC,DPU,Customer,Config
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import os
import tempfile
from django.contrib import admin
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
import os
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.html import format_html

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

# admin.py

from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Config

class ConfigAdmin(admin.ModelAdmin):
    list_display = ('user', 'st_id', 'timestamp', 'text_data', 'download_link')
    readonly_fields = ('download_link',)

    def download_link(self, obj):
        if obj.st_id:
            download_url = f'/admin/common/config/download/{obj.st_id}/'
            return mark_safe(f'<a href="{download_url}" target="_blank">Download</a>')
        return 'N/A'

    download_link.allow_tags = True
    download_link.short_description = 'Download'

admin.site.register(Config, ConfigAdmin)
