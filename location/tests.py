import datetime
import json

from django.urls import reverse
from rest_framework.test import APITestCase

from location.models import Country, City, Region
from location.serializers import CountryBaseSerializer
from user_profile.models import UserProfilePhoneVerification, UserProfile
from django.utils.translation import gettext as _


class UserCProfileTestCase(APITestCase):

    @staticmethod
    def _raw_location_data():
        return [
            {
                'country': {'name': 'Iran'},
                'cities': [
                    {
                        'pk': 1,
                        'name': 'Shiraz',
                        'regions': [
                            {
                                'name': 'Molasadra',
                                'lat': 1,
                                'lon': 2
                            },
                            {
                                'name': 'Zand',
                                'lat': 4,
                                'lon': 3
                            }
                        ]
                    },
                    {
                        'pk': 2,
                        'name': 'Tehran',
                        'regions': [
                            {
                                'name': 'Vanak',
                                'lat': 5,
                                'lon': 7
                            },
                            {
                                'name': 'Azadi',
                                'lat': 1.1,
                                'lon': 5.4
                            },
                            {
                                'name': 'Sharif',
                                'lat': 4.1,
                                'lon': 1.4
                            }
                        ]
                    },
                ]
            },
            {
                'country': {'name': 'UK'},
                'cities': [
                    {
                        'pk': 3,
                        'name': 'London',
                        'regions': [
                            {
                                'name': 'Times Square',
                                'lat': 0.3,
                                'lon': 1.4
                            }
                        ]
                    }
                ]
            }
        ]

    def setUp(self) -> None:
        self.countries = []
        self.cities = []
        self.regions = []

        self.populate_database()

    def populate_database(self):
        for _raw_data in self._raw_location_data():
            _country = Country.objects.create(**_raw_data.get('country'))
            self.countries.append(_country)

            for _city_data in _raw_data.get('cities'):
                _city = City.objects.create(country=_country, name=_city_data.get('name'))
                self.cities.append(_city)

                for _region_data in _city_data.get('regions'):
                    self.regions.append(Region.objects.create(city=_city, **_region_data))

    def get_countries_serialized(self):
        return [{
            'pk': _country.pk,
            'name': _country.name
        } for _country in self.countries]

    def get_cities_serialized(self):
        return [{
            'pk': city.pk,
            'name': city.name,
            'country': city.country.pk
        } for city in self.cities]

    def get_regions_serialized(self):
        return [{
            'pk': region.pk,
            'name': region.name,
            'city': region.city.pk,
            'lat': region.lat,
            'lon': region.lon
        } for region in self.regions]

    def test_list_countries(self):
        endpoint = reverse('location:country-list')
        response = self.client.get(endpoint)

        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response_data, self.get_countries_serialized())

    def test_list_cities(self):
        endpoint = reverse('location:city-list')
        response = self.client.get(endpoint)

        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response_data, self.get_cities_serialized())

    def test_list_cities_filter_country(self):
        endpoint = reverse('location:city-list')
        response = self.client.get(endpoint, {'country': 1})

        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)

        _cities_data = []
        for _city_data in self.get_cities_serialized():
            if _city_data.get('country') == 1:
                _cities_data.append(_city_data)

        self.assertListEqual(response_data, _cities_data)

    def test_list_cities_search_country_name(self):
        endpoint = reverse('location:city-list')
        response = self.client.get(endpoint, {'search': 'Iran'})

        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 2)

    def test_list_cities_search_name(self):
        endpoint = reverse('location:city-list')
        response = self.client.get(endpoint, {'search': 'Shiraz'})

        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 1)

    def test_list_regions(self):
        endpoint = reverse('location:region-list')
        response = self.client.get(endpoint)

        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response_data, self.get_regions_serialized())

    def test_list_regions_filter_city(self):
        endpoint = reverse('location:region-list')
        response = self.client.get(endpoint, {'city': 2})

        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 3)

    def test_list_regions_filter_country(self):
        endpoint = reverse('location:region-list')
        response = self.client.get(endpoint, {'city__country': 1})

        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 5)

    def test_list_regions_search_country(self):
        endpoint = reverse('location:region-list')
        response = self.client.get(endpoint, {'search': "UK"})

        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 1)

    def test_list_regions_search_city(self):
        endpoint = reverse('location:region-list')
        response = self.client.get(endpoint, {'search': "Shiraz"})

        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 2)
