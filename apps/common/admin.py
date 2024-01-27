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




from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from .models import Config

@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('user', 'st_id','text_data', 'timestamp')
    actions = ['download_lines']

    @user_passes_test(lambda u: u.is_staff)
    def download_lines(self, request, config_id):
        config_instance = get_object_or_404(Config, id=config_id)

        # Process config_instance.text_data to get the content you want to include in the response
        lines = config_instance.text_data.split('\n')
        content = "\n".join(lines)

        response = HttpResponse(content, content_type="text/plain")
        response['Content-Disposition'] = f'attachment; filename="config_lines.txt"'
        return response