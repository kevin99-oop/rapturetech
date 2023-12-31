from django.contrib import admin
from apps.common.models import DREC,DPU

# Register your models here.
@admin.register(DPU)
class DPUAdmin(admin.ModelAdmin):
    list_display = ('location', 'dpu_id', 'society', 'mobile_number', 'owner', 'status')

@admin.register(DREC)
class DRECAdmin(admin.ModelAdmin):
    list_display = ('id', 'REC_TYPE', 'SLIP_TYPE', 'ST_ID', 'CUST_ID', 'RecordingDate', 'END_TAG', 'dpuid')
    search_fields = ('REC_TYPE', 'SLIP_TYPE', 'ST_ID', 'CUST_ID', 'dpuid')  # Add fields you want to be searchable