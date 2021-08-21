from rest_framework import serializers

from diabo.models import DiaboProfile, Job
from user_profile.serializers import UserProfileBaseSerializer


class JobBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['pk', 'title', 'parent']


class DiaboProfileBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaboProfile
        fields = ['pk', 'user_profile', 'diabetes_type', 'job']


class DiaboProfileRetrieveSerializer(DiaboProfileBaseSerializer):
    user_profile = UserProfileBaseSerializer()
    job = JobBaseSerializer()


class DiaboProfileUpdateSerializer(DiaboProfileBaseSerializer):
    pass

