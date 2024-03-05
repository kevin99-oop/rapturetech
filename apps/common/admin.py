from django.contrib import admin
from apps.common.models import DREC,DPU,Customer,Config,RateTable,CustomerList
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

# Admin for DPU model
class DPUAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'dpu_id', 'society', 'mobile_number', 'owner', 'status', 'Amount', 'CAmount')
admin.site.register(DPU)

# Admin for DREC model
@admin.register(DREC)
class DRECAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the DREC admin interface
    list_display = ('REC_TYPE', 'SLIP_TYPE', 'ST_ID', 'CUST_ID', 'RecordingDate', 'SHIFT', 'QT', 'Amount', 'CAmount', 'dpuid')
    search_fields = ['ST_ID', 'CUST_ID']  # Add fields you want to search on

# Admin for Customer model
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the Customer admin interface
    list_display = ('user', 'st_id', 'csv_file','date_uploaded')
    search_fields = ('user__username', 'st_id')

class CustomerListAdmin(admin.ModelAdmin):
    list_display = ('user', 'st_id', 'cust_id', 'name', 'mobile', 'adhaar', 'bank_ac', 'ifsc')
    list_filter = ('user', 'st_id', 'cust_id')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # Apply additional filtering based on user, st_id, cust_id
        user_id = request.user.id
        st_id = request.GET.get('st_id', None)
        cust_id = request.GET.get('cust_id', None)

        if st_id:
            queryset = queryset.filter(st_id=st_id)
        if cust_id:
            queryset = queryset.filter(cust_id=cust_id)
        if not request.user.is_superuser:
            queryset = queryset.filter(user_id=user_id)

        return queryset

admin.site.register(CustomerList, CustomerListAdmin)
# Admin for Config model
@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the Config admin interface
    list_display = ('user', 'st_id', 'timestamp', 'text_data', 'download_link')
    readonly_fields = ('download_link',)

    def download_link(self, obj):
        # Generate a download link for Config model
        st_id = obj.st_id
        if st_id:  # Check if st_id is not empty
            download_url = reverse('download_config_by_st_id', args=[st_id])
            return format_html('<a href="{}" target="_blank">Download</a>', download_url)
        return "No st_id available"  # Provide a fallback message if st_id is empty

    download_link.short_description = 'Download'  # Define the display name for the download link

@admin.register(RateTable)
class RateTableAdmin(admin.ModelAdmin):
    list_display = ('user', 'animal_type', 'rate_type', 'start_date', 'csv_file', 'download_link')

    def download_link(self, obj):
        return f'<a href="{obj.csv_file.url}" download>Download</a>'

    download_link.allow_tags = True
    download_link.short_description = 'Download'

    def get_download_url(self, obj):
        return obj.csv_file.url