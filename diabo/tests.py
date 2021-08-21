import datetime
import json

from django.urls import reverse
from rest_framework.test import APITestCase

from location.models import Region, City, Country
from user_profile.models import UserProfilePhoneVerification, UserProfile
from django.utils.translation import gettext as _


class UserCProfileTestCase(APITestCase):

    def test_create_user_profile_with_diabo_profile(self):
        endpoint = reverse('diabo:profile_create')
