from django.urls import path

from user_profile.views import UserProfileSendCodeView, GetUserInfoView, UserProfileRUD

app_name = "user_profile"

urlpatterns = [
    path('send-code/',  UserProfileSendCodeView.as_view(), name="send_code"),
    path('verify-code/',  GetUserInfoView.as_view(), name="get_user_info"),
    path('user-profile/',  UserProfileRUD.as_view(), name="user_profile_retrieve_update"),

]

