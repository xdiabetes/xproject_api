from rest_framework import serializers

from diabetes_therapy.models import TherapyType


class TherapyTypeBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = TherapyType
        fields = ['pk', 'name']
