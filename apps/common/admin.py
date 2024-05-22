from django.contrib import admin
from apps.common.models import DREC,DPU,Customer,Config,RateTable,CustomerList,Questions
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

# Admin for DPU model
class DPUAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'zone', 'location', 'st_id', 'society', 'mobile_number', 'owner',
        'status', 'select_dpu'
    )
    list_filter = ('user', 'status', 'location', 'society')  # Add more fields as needed
    search_fields = ('user__username', 'location', 'st_id', 'society', 'mobile_number', 'owner')  # Add more fields as needed

admin.site.register(DPU, DPUAdmin)

# Admin for DREC model
@admin.register(DREC)
class DRECAdmin(admin.ModelAdmin):
  # Display all fields in the admin interface
    list_display = (
        'REC_TYPE', 'SLIP_TYPE', 'ST_ID', 'CUST_ID', 'TotalFileRecord', 'FlagEdited',
        'MType', 'RecordingDate', 'RecordingTime', 'SHIFT', 'FAT', 'FAT_UNIT',
        'SNF', 'SNF_UNIT', 'CLR', 'CLR_UNIT', 'WATER', 'WATER_UNIT', 'QT',
        'QT_UNIT', 'RATE', 'Amount', 'CAmount', 'CSR_NO', 'CREV', 'END_TAG',
        'dpuid', 'created_at','RID'
    )
    search_fields = ['ST_ID__st_id', 'CUST_ID']  # Add fields you want to search on
# Admin for Customer model
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the Customer admin interface
    list_display = ('user', 'st_id', 'csv_file', 'date_uploaded')
    search_fields = ('user__username', 'st_id')
    list_filter = ('user', 'st_id')
    
@admin.register(CustomerList)
class CustomerList(admin.ModelAdmin):
    list_display = ('user', 'st_id', 'cust_id', 'name', 'mobile', 'adhaar', 'bank_ac', 'ifsc')
    list_filter = ('user', 'st_id', 'cust_id')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # Apply additional filtering based on user, st_id, cust_id
        user_id = request.user.id
        user_filter = request.GET.get('user', None)
        st_id_filter = request.GET.get('st_id', None)
        cust_id_filter = request.GET.get('cust_id', None)

        if user_filter:
            queryset = queryset.filter(user=user_filter)
        if st_id_filter:
            queryset = queryset.filter(st_id=st_id_filter)
        if cust_id_filter:
            queryset = queryset.filter(cust_id=cust_id_filter)
        if not request.user.is_superuser:
            queryset = queryset.filter(user_id=user_id)

        return queryset


from django.contrib import admin
from apps.common.models import Config
from django.urls import reverse
from django.utils.html import format_html

@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('user', 'st_id', 'timestamp', 'text_data', 'download_link')
    readonly_fields = ('download_link',)
    search_fields = ('user', 'st_id')

    def download_link(self, obj):
        st_id = obj.st_id
        if st_id:
            download_url = reverse('download_config_by_st_id', args=[st_id])
            return format_html('<a href="{}" target="_blank">Download</a>', download_url)
        return "No st_id available"

    download_link.short_description = 'Download'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # Apply additional filtering based on user and st_id
        user_id = request.user.id
        user_filter = request.GET.get('user', None)
        st_id_filter = request.GET.get('st_id', None)

        if user_filter:
            queryset = queryset.filter(user=user_filter)
        if st_id_filter:
            queryset = queryset.filter(st_id=st_id_filter)
        if not request.user.is_superuser:
            queryset = queryset.filter(user_id=user_id)

        return queryset

from django.contrib import admin
from apps.common.models import RateTable
from django.utils.html import format_html

@admin.register(RateTable)
class RateTableAdmin(admin.ModelAdmin):
    list_display = ('user', 'animal_type', 'rate_type', 'start_date', 'csv_file', 'download_link')
    list_filter = ('user', 'animal_type', 'rate_type')

    def download_link(self, obj):
        return format_html('<a href="{}" download>Download</a>', obj.csv_file.url)

    download_link.short_description = 'Download'

    def get_download_url(self, obj):
        return obj.csv_file.url

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # Apply additional filtering based on user, animal_type, rate_type
        user_id = request.user.id
        animal_type = request.GET.get('animal_type', None)
        rate_type = request.GET.get('rate_type', None)

        if animal_type:
            queryset = queryset.filter(animal_type=animal_type)
        if rate_type:
            queryset = queryset.filter(rate_type=rate_type)
        if not request.user.is_superuser:
            queryset = queryset.filter(user_id=user_id)

        return queryset



@admin.register(Questions)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'admin_comment', 'asked_date']
