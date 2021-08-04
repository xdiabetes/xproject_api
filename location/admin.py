from django.contrib import admin
from .models import *


class CountryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    search_fields = ['name']


class CityAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'country']
    search_fields = ['name', 'country__name']


class RegionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'city', 'country']
    search_fields = ['name', 'city__name', 'city__country__name']


admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Region, RegionAdmin)
