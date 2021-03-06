from rest_framework import generics

from diabetes_therapy.helpers import therapy_serializers
from diabetes_therapy.models import TherapyCategory
from diabetes_therapy.serializes import TherapyTypeBaseSerializer
from user_profile.permissions import IsSuperUser


class TherapyCategoryCreateView(generics.CreateAPIView):
    permission_classes = (IsSuperUser, )
    serializer_class = TherapyTypeBaseSerializer


class TherapyCategoryListView(generics.ListAPIView):
    serializer_class = TherapyTypeBaseSerializer
    queryset = TherapyCategory.objects.all()


class TherapyCreateView(generics.CreateAPIView):

    def get_serializer_class(self):
        mode = self.kwargs.get('therapy_mode', None)
        return therapy_serializers.get(mode)
