from rest_framework import serializers

from diabo.models import DiaboProfile
from job.serializers import JobBaseSerializer
from user_profile.serializers import UserProfileBaseSerializer


class DiaboProfileBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaboProfile
        fields = ['pk', 'user_profile', 'diabetes_type', 'job']


class DiaboProfileRetrieveSerializer(DiaboProfileBaseSerializer):
    user_profile = UserProfileBaseSerializer()
    job = JobBaseSerializer()


class DiaboProfileUpdateSerializer(DiaboProfileBaseSerializer):
    pass

