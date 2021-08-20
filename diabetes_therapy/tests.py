import json

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse

from diabetes_therapy.models import TherapyCategory, Therapy
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
        self.therapy_categories = []

        self.create_sample_therapy_categories()

    def create_sample_therapy_categories(self):
        for therapy_category_data in self.get_raw_therapy_categories_data():
            self.therapy_categories.append(TherapyCategory.objects.create(**therapy_category_data))

    @staticmethod
    def get_raw_therapy_categories_data():
        return [
            {'name': 'Insulin'},
            {'name': 'pills'}
        ]

    def get_therapy_categories_serialized(self):
        return [{'pk': tt.pk, 'name': tt.name} for tt in self.therapy_categories]

    def test_create_therapy_category_super_user_should_get_201(self):
        endpoint = reverse('diabetes_therapy:therapy_category_create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser.token)
        request = self.client.post(endpoint, data={'name': 'Insulin'})
        self.assertEqual(request.status_code, 201)

    def test_create_therapy_category_normal_user_should_get_403(self):
        endpoint = reverse('diabetes_therapy:therapy_category_create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_user.token)
        request = self.client.post(endpoint, data={'name': 'Insulin'})
        self.assertEqual(request.status_code, 403)

    def test_list_therapy_categories(self):
        endpoint = reverse('diabetes_therapy:therapy_category_list_basic')
        request = self.client.get(endpoint)
        content = json.loads(request.content)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(content, self.get_therapy_categories_serialized())

    def test_fix_therapy_create_superuser_201(self):
        endpoint = reverse('diabetes_therapy:therapy_create', kwargs={'therapy_mode': Therapy.FIX})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser.token)
        request = self.client.post(endpoint, data={'type': self.therapy_categories[0].pk, 'name': 'fix test 1'})

        self.assertEqual(request.status_code, 201)
