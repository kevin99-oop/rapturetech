# apps/common/admin.py

from django.contrib import admin
from .models import DPU, DREC

@admin.register(DPU)
class DPUAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'dpu_id', 'society', 'mobile_number', 'owner', 'status')
    search_fields = ('user__username', 'dpu_id', 'society')

@admin.register(DREC)
class DRECAdmin(admin.ModelAdmin):
    list_display = ('dpu', 'st_id', 'recording_date', 'shift', 'amount', 'csr_no', 'crev')
    search_fields = ('dpu__user__username', 'st_id', 'recording_date')
