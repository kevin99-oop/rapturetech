from django.contrib import admin

# Register your models here.
from apps.common.models import DREC,DPU,Customer,TextFile


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
    list_display = ('user', 'st_id', 'csv_file')
    search_fields = ('user__username', 'st_id')

# admin.py
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from apps.common.models import TextFile

class TextFileAdmin(admin.ModelAdmin):
    list_display = ['user', 'st_id', 'file_link', 'formatted_upload_date']
    search_fields = ['user__username', 'st_id']
    list_filter = ['user']
    actions = ['download_selected_files']

    def file_link(self, obj):
        # Display a clickable link to download the file
        if obj.file:
            return format_html('<a href="{}" download>Download</a>', obj.file.url)
        return '-'
    file_link.short_description = 'File Link'

    def download_selected_files(modeladmin, request, queryset):
        # Create a zip file containing the selected text files
        import zipfile
        from io import BytesIO

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for text_file in queryset:
                # Add each file to the zip archive
                zip_file.write(text_file.file.path, arcname=f"{text_file.user.username}_{text_file.st_id}.txt")

        # Create a response with the zip file
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=text_files.zip'
        return response
    download_selected_files.short_description = 'Download Selected Files'

    def formatted_upload_date(self, obj):
        # Format the upload_date for display in the admin
        return obj.upload_date.strftime('%Y-%m-%d %H:%M:%S')
    formatted_upload_date.short_description = 'Upload Date'

admin.site.register(TextFile, TextFileAdmin)
