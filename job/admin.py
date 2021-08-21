from django.contrib import admin
from .models import *


class JobAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'parent']
    list_filter = ['parent']
    search_fields = ['title', 'parent__title']


admin.site.register(Job, JobAdmin)
