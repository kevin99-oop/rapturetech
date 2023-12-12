from django.contrib import admin

from .models import Profile

class UserProfile(admin.ModelAdmin):
    list_display=('id','username','bio')

admin.site.register(Profile)