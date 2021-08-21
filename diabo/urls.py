from django.urls import path

from diabo.views import DiaboProfileCreate, DiaboProfileRetrieve

app_name = 'diabo'

urlpatterns = [
    path('profile/create/', DiaboProfileCreate.as_view(), name='profile_create'),
    path('profile/retrieve/', DiaboProfileRetrieve.as_view(), name='profile_retrieve'),
    path('profile/update/', DiaboProfileRetrieve.as_view(), name='profile_update'),
]