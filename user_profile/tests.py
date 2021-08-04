import datetime
import json

from django.urls import reverse
from rest_framework.test import APITestCase

from location.models import Region, City, Country
from user_profile.models import UserProfilePhoneVerification, UserProfile
from django.utils.translation import gettext as _


class UserCProfileTestCase(APITestCase):

    def test_user_profile_send_code_endpoint(self):
        send_code_endpoint = reverse('user_profile:send_code')
        self.sendCodeAndAssert201(send_code_endpoint)

    def test_user_profile_send_code_two_times(self):
        send_code_endpoint = reverse('user_profile:send_code')
        self.sendCodeAndAssert201(send_code_endpoint)

        # user needs two wait at least TRY_BUFFER times
        response = self.client.post(send_code_endpoint, data={'phone_number': "09303131503"})
        self.assertEqual(response.status_code, 400)

    def test_user_profile_send_code_get_the_code(self):
        send_code_endpoint = reverse('user_profile:send_code')
        get_user_info_endpoint = reverse('user_profile:get_user_info')

        response = self.sendCodeAndAssert201(send_code_endpoint)
        api_response = json.loads(response.content)

        code = api_response.get('code')

        # we should be able to get the user info with the given code
        response = self.client.post(get_user_info_endpoint, data={'phone_number': "09303131503", 'code': code})
        api_response = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(api_response.get('phone_number'), "09303131503")

    def sendCodeAndAssert201(self, send_code_endpoint):
        response = self.client.post(send_code_endpoint, data={'phone_number': "09303131503"})
        self.assertEqual(response.status_code, 201)
        return response

    def test_user_profile_send_code_enter_wrong(self):
        send_code_endpoint = reverse('user_profile:send_code')
        get_user_info = reverse('user_profile:get_user_info')

        self.sendCodeAndAssert201(send_code_endpoint)

        for i in range(UserProfilePhoneVerification.MAX_QUERY):
            # 400 error should happen, because code is wrong
            response = self.client.post(get_user_info, data={'phone_number': "09303131503", 'code': "wrong1"})
            api_response = json.loads(response.content)

            self.assertEqual(response.status_code, 400)
            self.assertEqual(api_response.get('remaining_query_times'),
                             UserProfilePhoneVerification.MAX_QUERY - (i + 1))

        # phone number not found must happen
        response = self.client.post(get_user_info, data={'phone_number': "09303131503", 'code': "wrong1"})
        api_response = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(api_response.get('phone_number'),
                         _("Phone number not found"))

    def test_user_profile_send_code_wrong_code_right_code(self):
        send_code_endpoint = reverse('user_profile:send_code')
        get_user_info = reverse('user_profile:get_user_info')

        response = self.client.post(send_code_endpoint, data={'phone_number': "09303131503"})
        api_response = json.loads(response.content)
        self.assertEqual(response.status_code, 201)

        code = api_response.get('code')

        # wrong code first
        response = self.client.post(get_user_info, data={'phone_number': "09303131503", 'code': "wrong"})
        api_response = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(api_response.get('remaining_query_times'), UserProfilePhoneVerification.MAX_QUERY - 1)

        # send right code
        response = self.client.post(get_user_info, data={'phone_number': "09303131503", 'code': code})

        self.assertEqual(response.status_code, 200)

    def test_user_profile_send_code_verify_and_send(self):
        send_code_endpoint = reverse('user_profile:send_code')
        get_user_info = reverse('user_profile:get_user_info')

        response = self.client.post(send_code_endpoint, data={'phone_number': "09303131503"})
        api_response = json.loads(response.content)
        self.assertEqual(response.status_code, 201)

        code = api_response.get('code')

        # we should be able to get the user info with the given code
        response = self.client.post(get_user_info, data={'phone_number': "09303131503", 'code': code})
        api_response = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(api_response.get('phone_number'), "09303131503")

        # this should pass
        self.sendCodeAndAssert201(send_code_endpoint)

    def test_user_profile_auth_token_login(self):
        send_code_endpoint = reverse('user_profile:send_code')
        get_user_info = reverse('user_profile:get_user_info')
        update_user_profile_info = reverse('user_profile:user_profile_retrieve_update')

        response = self.client.post(send_code_endpoint, data={'phone_number': "09303131503"})
        api_response = json.loads(response.content)
        self.assertEqual(response.status_code, 201)

        code = api_response.get('code')

        # we should be able to get the user info with the given code
        response = self.client.post(get_user_info, data={'phone_number': "09303131503", 'code': code})
        api_response = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(api_response.get('phone_number'), "09303131503")
        self.assertEqual(api_response.get('first_name'), None)
        self.assertEqual(api_response.get('last_name'), None)

        # before authorization 401 must be returned
        response_401 = self.client.get(update_user_profile_info)
        self.assertEqual(response_401.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + api_response.get('token'))
        response = self.client.get(update_user_profile_info)
        api_response = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(api_response.get('phone_number'), "09303131503")
        self.assertEqual(api_response.get('first_name'), None)
        self.assertEqual(api_response.get('last_name'), None)

    def test_user_profile_update(self):
        send_code_endpoint = reverse('user_profile:send_code')
        get_user_info = reverse('user_profile:get_user_info')
        update_user_profile_info = reverse('user_profile:user_profile_retrieve_update')

        response = self.client.post(send_code_endpoint, data={'phone_number': "09303131503"})
        api_response = json.loads(response.content)
        self.assertEqual(response.status_code, 201)

        code = api_response.get('code')

        # we should be able to get the user info with the given code
        response = self.client.post(get_user_info, data={'phone_number': "09303131503", 'code': code})
        api_response = json.loads(response.content)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + api_response.get('token'))

        region = self.create_region()

        new_user_profile_data = {
            'phone_number': '09303131503',
            'first_name': 'Ali',
            'last_name': 'Parvizi',
            'nick_name': 'Sina',
            'gender': UserProfile.MALE,
            'diabetes_type': UserProfile.D_TYPE_1,
            'birth_date': datetime.datetime.now().date(),
            'location': region.pk,
        }
        response = self.client.put(update_user_profile_info, data=new_user_profile_data)
        api_response = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(api_response.keys(), new_user_profile_data.keys())

    @staticmethod
    def create_region():
        return Region.objects.create(
            **{
                'name': "Parse",
                'city': City.objects.create(**{
                    'country': Country.objects.create(name="Iran"),
                    'name': 'shiraz'
                })
            }
        )
