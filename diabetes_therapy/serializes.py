from rest_framework import serializers

from diabetes_therapy.models import TherapyCategory, Therapy, FixTherapy


class TherapyTypeBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = TherapyCategory
        fields = ['pk', 'name']


class TherapyBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Therapy
        fields = ['pk', 'order', 'name', 'type']
        abstract = True


class FixTherapyBaseSerializer(TherapyBaseSerializer):
    class Meta(TherapyBaseSerializer.Meta):
        model = FixTherapy
