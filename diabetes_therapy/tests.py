import json

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse

from diabetes_therapy.models import TherapyType
from user_profile.models import UserProfile


class DiaboTests(APITestCase):

    @staticmethod
    def create_superuser_user_profile(phone_number):
        _user = User.objects.create(username=phone_number, is_superuser=True)
        return UserProfile.objects.create(user=_user, phone_number=phone_number)

    @staticmethod
    def create_normal_user_profile(phone_number):
        _user = User.objects.create(username=phone_number, is_superuser=False)
        return UserProfile.objects.create(user=_user, phone_number=phone_number)

    def setUp(self) -> None:
        self.superuser = self.create_superuser_user_profile(phone_number="09017938091")
        self.normal_user = self.create_normal_user_profile(phone_number="09212422065")
        self.therapy_types = []

        self.create_sample_therapy_types()

    def create_sample_therapy_types(self):
        for therapy_type_data in self.get_raw_therapy_types_data():
            self.therapy_types.append(TherapyType.objects.create(**therapy_type_data))

    @staticmethod
    def get_raw_therapy_types_data():
        return [
            {'name': 'Insulin'},
            {'name': 'pills'}
        ]

    def get_therapy_types_serialized(self):
        return [{'pk': tt.pk, 'name': tt.name} for tt in self.therapy_types]

    def test_create_therapy_type_normal_user_should_get_403(self):
        endpoint = reverse('diabetes_therapy:therapy_type_create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_user.token)
        request = self.client.post(endpoint, data={'name': 'Insulin'})
        self.assertEqual(request.status_code, 403)

    def test_create_therapy_type_super_user_should_get_201(self):
        endpoint = reverse('diabetes_therapy:therapy_type_create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser.token)
        request = self.client.post(endpoint, data={'name': 'Insulin'})
        self.assertEqual(request.status_code, 201)

    def test_list_therapy_types(self):
        endpoint = reverse('diabetes_therapy:therapy_type_list')
        request = self.client.get(endpoint)
        content = json.loads(request.content)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(content, self.get_therapy_types_serialized())
