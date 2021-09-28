from django.db import models

from user_profile.models import UserProfile


class WalkingTrackerSession(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name="sessions", on_delete=models.CASCADE)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()


class WalkingSnapshot(models.Model):
    session = models.ForeignKey(WalkingTrackerSession, related_name="snapshots", on_delete=models.CASCADE)
    health_api_steps = models.IntegerField()
    pedometer_steps = models.IntegerField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    accuracy = models.FloatField(blank=True, null=True)
    altitude = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    speed_accuracy = models.FloatField(blank=True, null=True)
    heading = models.FloatField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
