from rest_framework import generics

from diabetes_therapy.models import TherapyType
from diabetes_therapy.permissions import IsSuperUser
from diabetes_therapy.serializes import TherapyTypeBaseSerializer


class TherapyTypeCreateView(generics.CreateAPIView):
    permission_classes = (IsSuperUser, )
    serializer_class = TherapyTypeBaseSerializer


class TherapyTypeListView(generics.ListAPIView):
    serializer_class = TherapyTypeBaseSerializer
    queryset = TherapyType.objects.all()

