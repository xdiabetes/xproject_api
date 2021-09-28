from rest_framework import serializers

from walking_tracker.models import WalkingTrackerSession, WalkingSnapshot


class WalkingSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalkingSnapshot
        fields = [
            'session',
            'location_data',
            'health_api_steps',
            'pedometer_steps',
            'latitude',
            'longitude',
            'accuracy',
            'altitude',
            'speed',
            'speed_accuracy',
            'heading',
            'datetime',
        ]


class WalkingTrackerSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalkingTrackerSession
        fields = [
            'start_date_time',
            'end_date_time',
        ]
