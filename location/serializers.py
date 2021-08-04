from rest_framework import serializers

from location.models import Country, City, Region, Address


class CountryBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['pk', 'name']


class CityBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['pk', 'name', 'country']


class CityDetailedSerializer(CityBaseSerializer):
    country = CountryBaseSerializer()


class RegionBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['pk', 'name', 'city', 'lat', 'lon']


class RegionDetailedSerializer(RegionBaseSerializer):
    city = CityDetailedSerializer()


class AddressBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['pk', 'raw_address', 'region', 'lat', 'lon']
