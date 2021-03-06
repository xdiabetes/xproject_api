import json

from django.urls import reverse
from rest_framework.test import APITestCase

from diabo.models import DiaboProfile
from job.models import Job

from user_profile.serializers import UserProfileBaseSerializer
from user_profile.tests import create_normal_user_profile


class DiaboProfileTests(APITestCase):

    def setUp(self) -> None:
        self.diabo_profile = self.get_sample_diabo_profile()
        self.user_profile_test = create_normal_user_profile(phone_number="09303131503")

    def do_login(self, user_profile=None):
        if not user_profile:
            user_profile = self.diabo_profile.user_profile
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_profile.token)

    @staticmethod
    def get_sample_diabo_profile():
        return DiaboProfile.objects.create(**{
            'user_profile': create_normal_user_profile(phone_number="09017938091"),
            'diabetes_type': DiaboProfile.D_TYPE_1,
            'job': Job.objects.create(title="Programmer")
        })

    def diabo_user_profile_serialized(self, diabo_profile=None):
        if not diabo_profile:
            diabo_profile = self.diabo_profile

        data = {
            'pk': diabo_profile.pk,
            'user_profile': UserProfileBaseSerializer(instance=diabo_profile.user_profile).data,
            'diabetes_type': diabo_profile.diabetes_type,
            'job': None
        }

        if diabo_profile.job:
            data['job'] = {
                'pk': diabo_profile.job.pk,
                'title': diabo_profile.job.title,
                'parent': diabo_profile.job.parent,
            }

        return data

    def test_get_diabo_profile_info_of_normal_user(self):
        endpoint = reverse('diabo:profile_retrieve')
        self.do_login(self.user_profile_test)
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            self.diabo_user_profile_serialized(
                DiaboProfile.get_or_create_from_user_profile(self.user_profile_test)
            )
        )

    def test_get_diabo_profile_info(self):
        self.do_login()
        endpoint = reverse('diabo:profile_retrieve')
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, json.dumps(self.diabo_user_profile_serialized()))

    def test_update_diabo_profile_diabetes_type(self):
        self.do_login()
        endpoint = reverse('diabo:profile_update')
        response = self.client.patch(endpoint, data={'diabetes_type': DiaboProfile.D_TYPE_2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content).get('diabetes_type', None), DiaboProfile.D_TYPE_2)


