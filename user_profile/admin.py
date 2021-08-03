from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['pk', 'phone_number', 'first_name', 'last_name', 'verification_status']


admin.site.register(UserProfile, UserProfileAdmin)
