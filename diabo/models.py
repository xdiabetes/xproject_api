from django.db import models

from job.models import Job
from user_profile.models import UserProfile
from django.utils.translation import gettext as _


class DiaboProfile(models.Model):
    D_TYPE_1 = '0'
    D_TYPE_2 = '1'

    diabetes_types = (
        (D_TYPE_1, _("Diabetes Type 1")),
        (D_TYPE_2, _("Diabetes Type 2")),
    )
    user_profile = models.OneToOneField(UserProfile, related_name="diabo_profile", on_delete=models.PROTECT)

    diabetes_type = models.CharField(max_length=1, choices=diabetes_types, blank=True, null=True)
    job = models.ForeignKey(Job, on_delete=models.PROTECT, blank=True, null=True)

    @staticmethod
    def get_or_create_from_user_profile(user_profile):
        try:
            return DiaboProfile.objects.get(user_profile=user_profile)
        except DiaboProfile.DoesNotExist:
            return DiaboProfile.objects.create(user_profile=user_profile)
