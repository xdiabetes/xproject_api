from rest_framework import generics

from diabo.models import DiaboProfile
from diabo.serializers import DiaboProfileRetrieveSerializer, DiaboProfileUpdateSerializer
from user_profile.permissions import IsLoggedIn


class DiaboProfileCreate(generics.CreateAPIView):
    pass


class DiaboProfileRetrieve(generics.RetrieveUpdateAPIView):
    permission_classes = (IsLoggedIn,)
    serializer_class = DiaboProfileRetrieveSerializer

    def get_object(self):
        user_profile = self.request.user.user_profile
        return DiaboProfile.get_or_create_from_user_profile(user_profile)


class DiaboProfileUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (IsLoggedIn,)
    serializer_class = DiaboProfileUpdateSerializer

    def get_object(self):
        user_profile = self.request.user.user_profile
        return DiaboProfile.get_or_create_from_user_profile(user_profile)
