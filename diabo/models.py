from django.db import models

from user_profile.models import UserProfile


class DiaboProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, related_name="diabo_profile", on_delete=models.PROTECT)
