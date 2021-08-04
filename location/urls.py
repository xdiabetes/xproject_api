from django.urls import path

from location.views import CountryListView, CityListView, RegionListView, RegionDetailedListView

app_name = 'location'

urlpatterns = [
    path('country/list/', CountryListView.as_view(), name="country-list"),
    path('city/list/', CityListView.as_view(), name="city-list"),
    path('region/list/', RegionListView.as_view(), name="region-list"),
    path('region/detailed/list/', RegionDetailedListView.as_view(), name="region-detailed-list"),
]
