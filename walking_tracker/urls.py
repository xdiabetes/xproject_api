from django.urls import path

from walking_tracker.views import SessionCreateView, session_create_test_view

app_name = "walking_tracker"

urlpatterns = [
    path('session/session_create_test_view/', session_create_test_view, name='session_create'),
    path('session/create/', SessionCreateView.as_view(), name='session_create'),
]