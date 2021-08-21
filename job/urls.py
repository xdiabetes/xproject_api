from django.urls import path

from diabo.views import JobCreateView, JobUpdateView, JobListView

app_name = 'job'

urlpatterns = [
    path('job/create/', JobCreateView.as_view(), name='job_create'),
    path('job/<int:job_id>/', JobUpdateView.as_view(), name='job_update'),
    path('job/list/', JobListView.as_view(), name='job_list'),
]