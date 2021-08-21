from rest_framework import generics

from diabo.models import DiaboProfile
from job.models import Job
from diabo.serializers import DiaboProfileRetrieveSerializer, DiaboProfileUpdateSerializer
from job.serializers import JobBaseSerializer
from user_profile.permissions import IsLoggedIn, IsSuperUser


class DiaboProfileRetrieve(generics.RetrieveUpdateAPIView):
    permission_classes = (IsLoggedIn,)
    serializer_class = DiaboProfileRetrieveSerializer

    def get_object(self):
        user_profile = self.request.user.user_profile
        return DiaboProfile.get_or_create_from_user_profile(user_profile)


class DiaboProfileUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (IsLoggedIn,)
    serializer_class = DiaboProfileUpdateSerializer

    def get_object(self):
        user_profile = self.request.user.user_profile
        return DiaboProfile.get_or_create_from_user_profile(user_profile)


class JobCreateView(generics.CreateAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = JobBaseSerializer


class JobUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = JobBaseSerializer

    queryset = Job.objects.all()

    lookup_field = 'pk'
    lookup_url_kwarg = 'job_id'

class JobListView(generics.ListAPIView):
    serializer_class = JobBaseSerializer
    queryset = Job.objects.all()
