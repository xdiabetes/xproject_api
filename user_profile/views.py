from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response

from user_profile.models import UserProfilePhoneVerification, UserProfile
from user_profile.permissions import IsLoggedIn
from user_profile.serializers import SendCodeSerializer, GetUserInfoSerializer, UserProfileBaseSerializer
from django.utils.translation import gettext as _


class UserProfileSendCodeView(generics.CreateAPIView):
    """
    Send User Profile SMS Code


    this endpoint create a pending user profile.
    """

    serializer_class = SendCodeSerializer


class UserProfileRUD(generics.RetrieveUpdateAPIView):
    permission_classes = (IsLoggedIn,)
    serializer_class = UserProfileBaseSerializer

    def get_object(self):
        return self.request.user.user_profile


class GetUserInfoView(generics.GenericAPIView):
    serializer_class = GetUserInfoSerializer

    def post(self, request, *args, **kwargs):
        serializer, user_profile = self.get_user_profile(request)
        vo = self.get_verification_object(user_profile)

        if not vo or not vo.is_usable:
            return Response({'phone_number': _("Phone number not found")}, status=400)

        if not self.is_code_correct(serializer, vo):
            return self.handle_wrong_code_and_return_response(vo)

        self.use_the_code(vo)
        return Response(UserProfileBaseSerializer(instance=user_profile).data)

    def handle_wrong_code_and_return_response(self, vo):
        remaining_query_times = self.handle_wrong_code_and_get_remaining_query_times(vo)
        return Response({'code': _("Incorrect Code"), 'remaining_query_times': remaining_query_times}, status=400)

    @staticmethod
    def use_the_code(vo):
        vo.used = True
        vo.save()

    @staticmethod
    def is_code_correct(serializer, vo):
        return vo.code == serializer.validated_data.get('code')

    @staticmethod
    def get_verification_object(user_profile):
        vo = UserProfilePhoneVerification.objects.last_not_expired_verification_object(user_profile=user_profile)
        return vo

    @staticmethod
    def handle_wrong_code_and_get_remaining_query_times(vo):
        # todo: anti concurrency
        vo.query_times += 1
        GetUserInfoView.burn_the_vo_if_maxed_out(vo)
        vo.save()
        remaining_query_times = UserProfilePhoneVerification.MAX_QUERY - vo.query_times
        return remaining_query_times

    @staticmethod
    def burn_the_vo_if_maxed_out(vo):
        if vo.query_times == UserProfilePhoneVerification.MAX_QUERY:
            vo.burnt = True

    def get_user_profile(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_profile = get_object_or_404(UserProfile, phone_number=serializer.validated_data.get('phone_number'))
        return serializer, user_profile
