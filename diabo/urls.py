from django.urls import path

from diabo.views import DiaboProfileCreate, DiaboProfileRetrieve, JobCreateView, JobListView, JobUpdateView

app_name = 'diabo'

urlpatterns = [
    path('profile/create/', DiaboProfileCreate.as_view(), name='profile_create'),
    path('profile/retrieve/', DiaboProfileRetrieve.as_view(), name='profile_retrieve'),
    path('profile/update/', DiaboProfileRetrieve.as_view(), name='profile_update'),

    path('job/create/', JobCreateView.as_view(), name='job_create'),
    path('job/<int:job_id>/', JobUpdateView.as_view(), name='job_update'),
    path('job/list/', JobListView.as_view(), name='job_list'),
]