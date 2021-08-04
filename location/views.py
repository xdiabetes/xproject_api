from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import filters

from location.models import Country, City, Region
from location.serializers import CountryBaseSerializer, CityBaseSerializer, RegionBaseSerializer, \
    RegionDetailedSerializer


class CountryListView(generics.ListAPIView):
    """
    List of all countries
    """
    serializer_class = CountryBaseSerializer
    queryset = Country.objects.all()


class CityListView(generics.ListAPIView):
    """
    List of all cities
    """

    serializer_class = CityBaseSerializer
    queryset = City.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['country']
    search_fields = ['country__name', 'name']


class RegionListView(generics.ListAPIView):
    """
    List of regions
    """

    serializer_class = RegionBaseSerializer
    queryset = Region.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city', 'city__country']
    search_fields = ['city__country__name', 'name', 'city__name']


class RegionDetailedListView(RegionListView):
    """
    List of regions with detailed city and country data
    """

    serializer_class = RegionDetailedSerializer
    