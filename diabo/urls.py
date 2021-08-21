from django.urls import path

from diabo.views import DiaboProfileRetrieve

app_name = 'diabo'

urlpatterns = [
    path('profile/retrieve/', DiaboProfileRetrieve.as_view(), name='profile_retrieve'),
    path('profile/update/', DiaboProfileRetrieve.as_view(), name='profile_update'),
]