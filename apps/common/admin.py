from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import DPU

class DPUDisplay(admin.ModelAdmin):
    list_display = ('location', 'dpu_id', 'society', 'mobile_number', 'owner', 'status')
    search_fields = ('location', 'dpu_id', 'society', 'mobile_number', 'owner')
    list_filter = ('status',)

admin.site.register(DPU, DPUDisplay)