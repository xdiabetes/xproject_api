from rest_framework import serializers

from job.models import Job


class JobBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['pk', 'title', 'parent']