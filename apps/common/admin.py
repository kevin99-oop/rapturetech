from django.contrib import admin

# Register your models here.
from apps.common.models import DREC,DPU,Customer,Config
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import os
import tempfile
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test

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
    actions = ['download_lines']

    @user_passes_test(lambda u: u.is_staff)
    def download_lines(self, request, queryset):
        try:
            # Create a temporary file to store the content
            temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w+')

            # Write the text content to the temporary file
            for config in queryset:
                line = f"{config.st_id} {config.created_at} {config.dputype} {config.rate_table}\n"
                temp_file.write(line)

            # Move the file cursor to the beginning for reading
            temp_file.seek(0)

            # Prepare the response for file download
            response = HttpResponse(temp_file, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="config_data.txt"'

            return response
        finally:
            # Close and delete the temporary file
            temp_file.close()
            os.unlink(temp_file.name)

    download_lines.short_description = "Download selected lines as TXT file"