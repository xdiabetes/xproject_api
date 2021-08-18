from rest_framework import generics

from diabetes_therapy.permissions import IsSuperUser
from diabetes_therapy.serializes import TherapyTypeCreateSerializer


class TherapyTypeCreateView(generics.CreateAPIView):
    permission_classes = (IsSuperUser, )
    serializer_class = TherapyTypeCreateSerializer
