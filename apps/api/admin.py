from django.contrib import admin
from .models import CtRecord, DRecord, DpuAsKcs, Dpus, RateTableAlls, RateTables

admin.site.register(CtRecord)
admin.site.register(DRecord)
admin.site.register(DpuAsKcs)
admin.site.register(Dpus)
admin.site.register(RateTableAlls)
admin.site.register(RateTables)