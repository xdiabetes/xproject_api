from django.utils.translation import ugettext as _
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response

from xapp.api_v1.consts import UserProfileConsts
from xapp.api_v1.permissions import IsLoggedIn
from xapp.api_v1.serializers.UserProfileSerializrs import UserProfileCRSerializer, UserProfileUpdateSerializer, \
    UserProfilePhoneVerificationSerializer, SendXprojectCodeSerializer
from xapp.models import UserProfilePhoneVerification, UserProfile
from xproject.secret import DEMO


class SendXprojectCode(generics.GenericAPIView):
    """
        Send Code.

        Send verification code.

        phone must have been registered before.

        if send failed respond with wait time.
    """

    serializer_class = SendXprojectCodeSerializer

    @staticmethod
    def get_user_profile(phone_number):
        try:
            return UserProfile.objects.get(phone_number=phone_number)
        except UserProfile.DoesNotExist:
            ups = UserProfileCRSerializer(data={'phone_number': phone_number})
            ups.is_valid(raise_exception=True)
            user_profile = ups.save()
            return user_profile

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        upv = UserProfilePhoneVerification.objects. \
            create(user_profile=self.get_user_profile(serializer.data.get('phone_number')))

        if upv['status'] != 201:
            return Response({'detail': _("Code not sent"), 'wait': upv['wait']}, status=upv['status'])

        if DEMO:
            return Response({"code": upv['obj'].code})

        return Response({'detail': _("Code sent")})

class UserProfileAuthTokenView(generics.GenericAPIView):
    """
        User Profile Auth token.

        match phone number and verification code.

        return user token on success.
    """

    serializer_class = UserProfilePhoneVerificationSerializer

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone_number')
        code = request.data.get('code')

        user_profile_phone_ = UserProfilePhoneVerification.objects.order_by('create_date'). \
            filter(
            query_times__lt=UserProfilePhoneVerification.MAX_QUERY,
            used=False,
            burnt=False,
            user_profile__phone_number=phone
        )
        user_profile_phone = user_profile_phone_.last()

        if not user_profile_phone:
            return Response({'detail': _('Phone number not found')}, status=status.HTTP_404_NOT_FOUND)

        if code != user_profile_phone.code:
            user_profile_phone.query_times += 1
            user_profile_phone.save()

            return Response({'detail': _('Invalid verification code'),
                             'allowed_retry_times':
                                 UserProfilePhoneVerification.MAX_QUERY -
                                 user_profile_phone.query_times},
                            status=status.HTTP_403_FORBIDDEN)

        user_profile_phone.user_profile.verification_status = UserProfileConsts.VERIFIED
        user_profile_phone.user_profile.save()
        token, created = Token.objects.get_or_create(user=user_profile_phone.user_profile.django_user)

        user_profile_phone.used = True
        user_profile_phone.save()

        # mark all other codes as burnt
        user_profile_phone_.update(burnt=True)

        return Response(self.serializer_class(instance=user_profile_phone.user_profile).data)

class UserProfileRUView(RetrieveUpdateAPIView):
    """
        User Profile Retrieve.

        Currently logged in User can retrieve and update itself.

        they cannot change their phone number.
    """

    serializer_class = UserProfileUpdateSerializer
    permission_classes = (IsLoggedIn,)

    def get_object(self):
        return self.request.user.user_profile