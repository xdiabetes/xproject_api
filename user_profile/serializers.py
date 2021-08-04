from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from rest_framework import serializers
from django.utils.translation import gettext as _

from location.serializers import RegionDetailedSerializer
from xproject.secret import DEBUG
from user_profile.helpers import send_verification_code
from user_profile.models import UserProfile, UserProfilePhoneVerification


class UserProfileBaseSerializer(serializers.ModelSerializer):
    location_detailed = RegionDetailedSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['pk', 'first_name', 'last_name', 'phone_number', 'verification_status', 'token',
                  'nick_name', 'gender', 'diabetes_type', 'birth_date', 'location', 'location_detailed']


class UserProfileGetOrCreateSerializerUsingPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', ]

    def create(self, validated_data):
        try:
            user_profile = UserProfile.objects.get(phone_number=validated_data.get('phone_number'))
        except UserProfile.DoesNotExist:
            user = User.objects.create(username=validated_data.get('phone_number'))
            user_profile = UserProfile.objects.create(**validated_data, user=user)

        return user_profile


class SendCodeSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[RegexValidator(
        regex=r"^(\+98|0)?9\d{9}$",
        message=_("Enter a valid phone number"),
        code='invalid_phone_number'),
    ], write_only=True)

    class Meta:
        model = UserProfilePhoneVerification
        fields = ['pk', 'create_date', 'query_times', 'phone_number']

        extra_kwargs = {
            'create_date': {'read_only': True},
            'query_times': {'read_only': True},
            'phone_number': {'read_only': True},
        }
        if DEBUG:
            fields += ['code']
            extra_kwargs['code'] = {'read_only': True}

    def create(self, validated_data):
        phone_number = validated_data.get('phone_number')
        user_profile = self.get_or_create_user_profile(phone_number, validated_data)
        verification_object = self.send_verification_sms(user_profile)

        return verification_object.get('obj')

    @staticmethod
    def send_verification_sms(user_profile):
        # send a verification sms to the given user_profile
        verification_object = user_profile.get_verification_object()
        if verification_object.get('status') != 201:
            raise serializers.ValidationError(verification_object)
        send_verification_code(user_profile.phone_number, verification_object.get('obj').code)
        return verification_object

    def get_or_create_user_profile(self, phone_number, validated_data):
        # get or create a user profile
        try:
            user_profile = UserProfile.objects.get(phone_number=phone_number)
        except UserProfile.DoesNotExist:
            user_profile = self.create_user_profile(validated_data)
        return user_profile

    @staticmethod
    def create_user_profile(validated_data):
        serializer = UserProfileGetOrCreateSerializerUsingPhoneNumberSerializer(data=validated_data)
        serializer.is_valid(raise_exception=True)
        user_profile = serializer.save()
        return user_profile


class GetUserInfoSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[RegexValidator(
        regex=r"^(\+98|0)?9\d{9}$",
        message=_("Enter a valid phone number"),
        code='invalid_phone_number'),
    ], write_only=True)
    code = serializers.CharField()

