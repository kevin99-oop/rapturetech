from django.contrib import admin

# Register your models here.
from apps.common.models import DREC,DPU,Customer


class DPUAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'dpu_id', 'society', 'mobile_number', 'owner', 'status', 'Amount', 'CAmount')
@admin.register(DREC)
class DRECAdmin(admin.ModelAdmin):
    list_display = ('REC_TYPE', 'SLIP_TYPE', 'ST_ID', 'CUST_ID', 'RecordingDate', 'SHIFT', 'QT', 'Amount', 'CAmount')
    search_fields = ['ST_ID', 'CUST_ID']  # Add fields you want to search on

    # Additional configurations as needed
admin.site.register(Customer)
admin.site.register(DPU)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mobile', 'adhaar', 'bank', 'ac', 'ifsc')
    search_fields = ('name', 'mobile', 'adhaar', 'bank', 'ac', 'ifsc')