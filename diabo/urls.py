from django.urls import path

from diabo.views import DiaboProfileCreate

app_name = 'diabo'

urlpatterns = [
    path('profile/create/', DiaboProfileCreate.as_view(), name='profile_create'),
]